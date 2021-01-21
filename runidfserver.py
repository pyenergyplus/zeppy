#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

"""server for run the eppy.modelmaker.IDF and wfile=filepath"""

import time
import zmq
import tempfile

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

import witheppy
import eppy
import witheppy.runandget as runandget

# idfname = "./idffolder/1ZoneUncontrolled.idf"
# wfile = "./idffolder/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"


while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Received request:")

    #  Do some 'work'
    idf, wfiletxt, getdict = message
    with tempfile.TemporaryDirectory() as tmpdir:
        idf_temp_file = f'{tmpdir}/a.idf'
        wfile_temp_file = f'{tmpdir}/a.epw'
        open(wfile_temp_file, 'w').write(wfiletxt)
        idf.saveas(idf_temp_file)
        print("saved temp files")
        idf_temp = eppy.openidf(idf_temp_file, epw=wfile_temp_file)
        fullresult = runandget.anon_runandget(idf_temp, getdict)
        print(fullresult)

    #  Send reply back to client
    socket.send_pyobj(fullresult)