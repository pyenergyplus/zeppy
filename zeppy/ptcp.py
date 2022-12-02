# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""parallel pipeline tcp functions"""


import time
import os.path
import string
import random
import multiprocessing
from datetime import date, datetime
from functools import wraps

import zmq


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")

    return _time_it


def randstr(strlength):
    """return a string of length strlength"""
    randletters = string.ascii_lowercase + string.digits
    return "".join([random.choice(randletters) for i in range(strlength)])


def _v_print(txt, verbose=False):
    """print if verbose==True"""
    if verbose:
        print(txt)


def _zmq_sink(verbose=False, sinkipc=None, killipc=None, resultipc=None):
    """zmq sink for rweather"""
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    # receiver.bind(sinkipc)
    receiver.bind("tcp://*:5558")

    # socket to publish end of tasks
    endpubliser = context.socket(zmq.PUB)
    # endpubliser.bind(killipc)
    endpubliser.bind("tcp://*:5555")

    # socket to publish results
    resultpubliser = context.socket(zmq.PUB)
    # resultpubliser.bind(resultipc)
    resultpubliser.bind("tcp://*:5556")

    num_calc = receiver.recv_pyobj()
    # num_calc = num_calc.decode()
    num_calc = int(num_calc)
    _v_print(f"number of calculations = {num_calc}", verbose=verbose)

    # Start our clock now
    tstart = time.time()

    allresults = list()
    for task_nbr in range(num_calc):
        s = receiver.recv_pyobj()
        allresults.append(s)

    # end the workers
    # print("sending end message")
    endpubliser.send(b"end this now")

    # publish the results
    # print("publishing the results")
    allresults.sort()  # make sure they are in the right order

    # remove order index and publish it
    resultpubliser.send_pyobj([line for _, line in allresults])
    # resultpubliser.send_pyobj(allresults)

    # Calculate and report duration of batch
    tend = time.time()
    _v_print(
        "Total taken time for all calcs: %d msec" % ((tend - tstart) * 1000),
        verbose=verbose,
    )


def _zmq_worker(
    func, wnum=None, verbose=False, sinkipc=None, killipc=None, ventipc=None
):
    """zmq worker for rweather"""
    if wnum is None:
        wnum = 0
    # use wnum, inc case you want to now which woker did the job
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    # receiver.connect(ventipc)
    receiver.connect("tcp://localhost:5557")

    # Socket to send messages to sink
    sender = context.socket(zmq.PUSH)
    # print(111,sinkipc)
    # sender.connect(sinkipc)
    sender.connect("tcp://localhost:5558")

    # socket to recieve end message to stop this worker
    endsubscriber = context.socket(zmq.SUB)
    # endsubscriber.connect(killipc)
    endsubscriber.connect("tcp://localhost:5555")
    endsubscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    poller.register(endsubscriber, zmq.POLLIN)

    # Process tasks forever
    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        if receiver in socks:
            try:
                i, task = receiver.recv_pyobj()
                _v_print(f"running item: {i}, in worker: {wnum}", verbose=verbose)
                # get the args and kwargs
                try:
                    args = task["args"]
                except KeyError as e:
                    args = list()
                try:
                    kwargs = task["kwargs"]
                except KeyError as e:
                    kwargs = dict()
                # Do the work
                result = func(*args, **kwargs)
                # Send results to sink with index number i
                sender.send_pyobj((i, result))
            except Exception as e:
                print("****ERROR****", e)
                _v_print(
                    f"****ERROR**** above error while running item: {i}, in worker: {wnum}",
                    verbose=True,
                )
                sender.send_pyobj((i, "****ERROR****"))
                # TODO send this as a log message to logger
            _v_print(
                f"sent result of item: {i}, in worker: {wnum} to sink", verbose=verbose
            )

        if endsubscriber in socks:
            message = endsubscriber.recv()
            break


def _zmq_vent(args_list, verbose=False, sleeptime=0.1, sinkipc=None, ventipc=None):
    """zmq vent for rweather"""
    context = zmq.Context()

    # Socket to send messages on
    sender = context.socket(zmq.PUSH)
    # print(171, ventipc)
    # sender.bind(ventipc)
    sender.bind("tcp://*:5557")

    # Socket with direct access to the sink: used to synchronize start of batch
    # if sink is not running at this point - whole thing gets fucked up
    sink = context.socket(zmq.PUSH)
    # sink.connect(sinkipc)
    sink.connect("tcp://localhost:5558")

    totwork = len(args_list)
    sink.send_pyobj(totwork)

    # total_msec = 0
    for i, task in enumerate(args_list):
        sender.send_pyobj((i, task))

        # Give 0MQ time to deliver - otherwise all of it will go to one worker
        # print(f"sleeptime={sleeptime}")
        time.sleep(sleeptime)


def _zmq_resultsub(verbose=False, resultipc=None):
    """get the results of the reweather calculations"""

    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # socket.connect(resultipc)
    socket.connect("tcp://localhost:5556")

    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    # print('started result subscriber')
    message = socket.recv_pyobj()
    return message


def _fan_out_in(
    func, args_list, nworkers=None, verbose=False, sleeptime=0.1, ipcs=None
):
    """Starts a distributed zmq run of `func`
    Each instance of `func` is run in a separate process
    Uses the classic patallel-pipeline from zmq
        - vent -> workers -> sink
    The results are published in PUB-SUB pattern"""
    sinkipc = ipcs["sinkipc"]
    killipc = ipcs["killipc"]
    resultipc = ipcs["resultipc"]
    ventipc = ipcs["ventipc"]

    # starts the workers
    if nworkers is None:
        nworkers = len(args_list)
    for i in range(nworkers):
        # for i in range(1):

        p = multiprocessing.Process(
            target=_zmq_worker,
            args=(
                func,
                i,
            ),
            kwargs={
                "verbose": verbose,
                "sinkipc": sinkipc,
                "killipc": killipc,
                "ventipc": ventipc,
            },
        )
        p.start()
        _v_print(f"started worker {i}", verbose=verbose)

    # Starts sink
    p = multiprocessing.Process(
        target=_zmq_sink,
        kwargs={
            "verbose": verbose,
            "sinkipc": sinkipc,
            "killipc": killipc,
            "resultipc": resultipc,
        },
    )
    p.start()
    _v_print("starting sink", verbose=verbose)

    # starts the vent
    p = multiprocessing.Process(
        target=_zmq_vent,
        args=(args_list,),
        kwargs={
            "verbose": verbose,
            "sleeptime": sleeptime,
            "sinkipc": sinkipc,
            "ventipc": ventipc,
        },
    )
    p.start()
    _v_print("started ventilator", verbose=verbose)


# ---


def _sinkipc(size=8):
    return f"ipc:///tmp/zeppysink_{randstr(size)}"


def _killipc(size=8):
    return f"ipc:///tmp/zeppykill_{randstr(size)}"


def _resultipc(size=8):
    return f"ipc:///tmp/zeppyresult_{randstr(size)}"


def _ventipc(size=8):
    return f"ipc:///tmp/zeppyvent_{randstr(size)}"


# ---


def _sinktcp():
    # return f"tcp://*:5558"
    return f"tcp://localhost:5558"


def _killtcp():
    return f"tcp://localhost:5555"


def _resulttcp():
    return f"tcp://localhost:5556"


def _venttcp():
    return f"tcp://localhost:5558"


# ---


def ipc_parallelpipe(func, args_list, nworkers=None, verbose=False, sleeptime=0.1):
    """distributed run of the func using zmq
    Returns the results of all the run
    Uses IPC"""
    args_list = args_kwargs_helper(args_list)
    # generate ipcs
    sz = 3
    ipcs = dict(
        sinkipc=_sinkipc(sz),
        killipc=_killipc(sz),
        resultipc=_resultipc(sz),
        ventipc=_ventipc(sz),
    )
    _fan_out_in(
        func,
        args_list,
        nworkers=nworkers,
        verbose=verbose,
        sleeptime=sleeptime,
        ipcs=ipcs,
    )
    # -> parallel-pipline publishing the results
    message = _zmq_resultsub(
        resultipc=ipcs["resultipc"]
    )  # subscribes to the published results

    return message


def tcp_parallelpipe(func, args_list, nworkers=None, verbose=False, sleeptime=0.1):
    """distributed run of the func using zmq
    Returns the results of all the run
    Uses TCP"""
    args_list = args_kwargs_helper(args_list)
    # generate ipcs
    # sz = 3
    tcps = dict(
        sinkipc=_sinktcp(),
        killipc=_killtcp(),
        resultipc=_resulttcp(),
        ventipc=_venttcp(),
    )
    _fan_out_in(
        func,
        args_list,
        nworkers=nworkers,
        verbose=verbose,
        sleeptime=sleeptime,
        ipcs=tcps,
    )
    # -> parallel-pipline publishing the results
    message = _zmq_resultsub(
        resultipc=tcps["resultipc"]
    )  # subscribes to the published results

    return message


def args_kwargs_helper(args_kwargs_list):
    return [clean_args_kwargs(item) for item in args_kwargs_list]


def clean_args_kwargs(args_kwargs):
    if isinstance(args_kwargs, dict):
        return args_kwargs
    if isinstance(args_kwargs, (list, tuple)):
        return {"args": args_kwargs, "kwargs": {}}
    return {"args": (args_kwargs,), "kwargs": {}}


# ---- the stuff above should be generic


def waitsome(seconds):
    """wait for some seconds"""
    time.sleep(seconds)
    return seconds


def wait_add(first, second):
    """wait for the sum of first and second. return the sum"""
    seconds = first + second
    return waitsome(seconds)


def wait_add_mult(first, add=0, mult=1):
    """calculate the result=(first+add)*mult. Then waitsome(result)"""
    result = (first + add) * mult
    return waitsome(result)


def idfversion(idf):
    versions = idf.idfobjects["version"]
    ver = versions[0]
    return ver.Version_Identifier


def eplaunch_run(idf):
    # import witheppy.runner
    # witheppy.runner.eplaunch_run(idf)
    # idf.run(output_directory='./eplus/', output_prefix='C')
    import subprocess
    import os.path

    wfile = idf.epw
    idfname = idf.idfname
    justname = os.path.basename(idfname).split(".")[0]
    dirname = os.path.dirname(idfname)
    runstr = f"/Applications/EnergyPlus-9-1-0/energyplus -d {dirname} -p {justname} -s C  -w {wfile} {idfname}"
    # runstr = f'/Applications/EnergyPlus-9-1-0/energyplus --help'
    # runargs = ['/Applications/EnergyPlus-9-1-0/energyplus', '-d ./eplus_files/ -p Minimal -s C ./eplus_files/Minimal.idf']
    subprocess.check_call(runstr.split())
    return None


def idf_run(idf):
    import witheppy.runner

    witheppy.runner.eplaunch_run(idf)
    # does not wirk with ppipes


def idf_multirun(idf_kwargs):
    import eppy

    idf = idf_kwargs["args"]
    options = idf_kwargs["kwargs"]
    idf.run(**options)


def make_options(idf):
    idfversion = idf.idfobjects["version"][0].Version_Identifier.split(".")
    idfversion.extend([0] * (3 - len(idfversion)))
    idfversionstr = "-".join([str(item) for item in idfversion])
    fname = idf.idfname
    options = {
        "ep_version": idfversionstr,
        "output_prefix": os.path.basename(fname).split()[0],
        "output_suffix": "C",
        "output_directory": os.path.dirname(fname),
    }
    return options


@measure
def runeverything():
    # waitlist = [1, 2, 3, 2, 1]
    # # waitlist = [(1, ), (2, ), (3, ), (2, ), (1, )]
    # # waitlist = [(1, 0), (1, 1), (2, 1), (2, 0), (0, 1)]
    # # waitlist = [(1, 0, 1), (1, 1, 1), (2, 1, 1), (2, 0, 1), (0, 1, 1)]
    # waitlist = [(1, 0, 1), (1, 1, 1), (2, 1, 1), (2, 0, 1), (0, 1, 1)]
    # # waitlist = [(1, 0, 1), ]
    # # waitlist = [{'args':(1, ), 'kwargs':{'add':0, 'mult':1}}]
    # waitlist = [
    #     # {'args':1, 'kwargs':{'add':3}},
    #     {'args':(1,), 'kwargs':{'mult':3}},
    #     {'args':(1,), 'kwargs':{'add':2, 'mult':3}},
    #     {'args': (1, 2, 3)},
    # ]
    # print(waitlist)
    # func = wait_add_mult
    # result = ipc_parallelpipe(func, waitlist, nworkers=None, verbose=True)
    #
    # print(result)

    # running eppy in zeppy
    import eppy

    fnames = [
        # "./eplus_files/Minimal.idf",
        "./eplus_files/UnitHeaterGasElec.idf",
        "./eplus_files/ZoneWSHP_wDOAS.idf",
        "./eplus_files/ZoneWSHP_wDOAS_1.idf",
    ]
    wfile = (
        "/Applications/EnergyPlus-9-1-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    )
    idfs = [eppy.openidf(fname, epw=wfile) for fname in fnames]
    waitlist = [[{"args": idf, "kwargs": make_options(idf)}] for idf in idfs]
    func = idf_multirun
    result = ipc_parallelpipe(func, waitlist, nworkers=None, verbose=True, sleeptime=1)
    # sleeptime=1 sec. This is a pause between sending the task out. Not sure if a single worker is grabbing all the tasks in E+. May need some testing to confirm.
    print(result)


if __name__ == "__main__":
    runeverything()
