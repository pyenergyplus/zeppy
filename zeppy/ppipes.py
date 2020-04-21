"""parallel pipeline functions"""

import zmq
import time

import multiprocessing

from datetime import date, datetime
from functools import wraps

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
    


def _v_print(txt, verbose=False):
    """print if verbose==True"""
    if verbose:
        print(txt)

def _zmq_sink(verbose=False):
    """zmq sink for rweather"""
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.bind("ipc:///tmp/5558")
    
    # socket to publish end of tasks
    endpubliser = context.socket(zmq.PUB)
    endpubliser.bind("ipc:///tmp/zmq_endpub")

    # socket to publish results
    resultpubliser = context.socket(zmq.PUB)
    resultpubliser.bind("ipc:///tmp/zmq_resultpuh")

    num_calc = receiver.recv_pyobj()
    # num_calc = num_calc.decode()
    num_calc = int(num_calc)
    _v_print(f'number of calculations = {num_calc}', verbose=verbose)

    # Start our clock now
    tstart = time.time()

    allresults = list()
    for task_nbr in range(num_calc):
        s = receiver.recv_pyobj()
        allresults.append(s)
    
    # end the workers
    # print("sending end message")
    endpubliser.send(b'end this now')
    
    # publish the results
    # print("publishing the results")
    allresults.sort() # make sure they are in the right order
    
    # remove order index and publish it
    resultpubliser.send_pyobj([line for _, line in allresults])
    # resultpubliser.send_pyobj(allresults)
    
    # Calculate and report duration of batch
    tend = time.time()
    _v_print("Total taken time for all calcs: %d msec" % ((tend-tstart)*1000), 
        verbose=verbose)

def _zmq_worker(func, wnum=None, verbose=False):
    """zmq worker for rweather"""
    if wnum is None:
        wnum = 0
    # use wnum, inc case you want to now which woker did the job
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.connect("ipc:///tmp/5557")

    # Socket to send messages to
    sender = context.socket(zmq.PUSH)
    sender.connect("ipc:///tmp/5558")
    
    # socket to recieve end message to stop this worker
    endsubscriber = context.socket(zmq.SUB)
    endsubscriber.connect("ipc:///tmp/zmq_endpub")
    endsubscriber.setsockopt_string(zmq.SUBSCRIBE, '')

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
            i, task = receiver.recv_pyobj()
            _v_print(f'running item: {i}, in worker: {wnum}', verbose=verbose)
            # get the args and kwargs
            try:
                args = task['args']
            except KeyError as e:
                args = list()
            try:
                kwargs = task['kwargs']
            except KeyError as e:
                kwargs = dict()
            # Do the work
            result = func(*args, **kwargs) 
            # Send results to sink with index number i
            sender.send_pyobj((i, result))
            
        if endsubscriber in socks:
            message = endsubscriber.recv()
            break
        
def _zmq_vent(args_list, verbose=False):
    """zmq vent for rweather"""

    context = zmq.Context()

    # Socket to send messages on
    sender = context.socket(zmq.PUSH)
    sender.bind("ipc:///tmp/5557")

    # Socket with direct access to the sink: used to synchronize start of batch
    # if sink is not running at this point - whole thing gets fucked up
    sink = context.socket(zmq.PUSH)
    sink.connect("ipc:///tmp/5558")

    totwork = len(args_list)
    sink.send_pyobj(totwork)

    # total_msec = 0
    for i, task in enumerate(args_list):
        sender.send_pyobj((i, task))

        # Give 0MQ time to deliver - otherwise all of it will go to one worker
        time.sleep(0.1)


def _zmq_resultsub(verbose=False):
    """get the results of the reweather calculations"""

    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect("ipc:///tmp/zmq_resultpuh")


    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    # print('started result subscriber')
    message = socket.recv_pyobj()
    return message


def _fan_out_in(func, args_list, nworkers=None, verbose=False):
    """Starts a distributed zmq run of `func` 
    Each instance of `func` is run in a separate process
    Uses the classic patallel-pipeline from zmq
        - vent -> workers -> sink
    The results are published in PUB-SUB pattern """
    
    # starts the workers
    if nworkers is None:
        nworkers = len(args_list)
    for i in range(nworkers):
    # for i in range(1):
        p = multiprocessing.Process(target=_zmq_worker, args=(func, i, ), kwargs={'verbose':verbose})
        p.start()
        _v_print(f'started worker {i}', verbose=verbose)
        
    # Starts sink
    p = multiprocessing.Process(target=_zmq_sink,  kwargs={'verbose':verbose})
    p.start()
    _v_print('started sink', verbose=verbose)

    # starts the vent
    p = multiprocessing.Process(target=_zmq_vent, args = (args_list, ),  kwargs={'verbose':verbose})
    p.start()
    _v_print('started vent', verbose=verbose)

def ipc_parallelpipe(func, args_list, nworkers=None, verbose=False):
    """distributed run of the func using zmq
    Returns the results of all the run"""
    args_list = arglist_helper(args_list)
    _fan_out_in(func, args_list, nworkers=nworkers, verbose=verbose) 
        # -> parallel-pipline publishing the results
    message = _zmq_resultsub() # subscribes to the published results
    return message
    
def arglist_helper(args_list):
    if isinstance(args_list[0], (tuple, list)):
        return [{'args':(*item, )} for item in args_list]
    else:
        return [{'args':(item, )} for item in args_list]
    
# ---- the stuff above should be generic

def waitsome(seconds):
    """wait for some seconds"""
    time.sleep(seconds)
    return seconds
    
if __name__ == '__main__':
    waitlist = [1, 2, 3, 2, 1]
    func = waitsome
    result = ipc_parallelpipe(func, waitlist, nworkers=None, verbose=True)    
    print(result)
    