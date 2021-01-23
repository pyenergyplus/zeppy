#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

"""server gets a text file of idf and wfile"""

import time
import zmq
import tempfile

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

import witheppy
import eppy
import witheppy.runandget as runandget

def zeppy_runandget(idftxt, wfiletxt, getdict):
    with tempfile.TemporaryDirectory() as tmpdir:
        idf_temp_file = f'{tmpdir}/a.idf'
        open(idf_temp_file, 'w').write(idftxt)
        wfile_temp_file = f'{tmpdir}/a.epw'
        open(wfile_temp_file, 'w').write(wfiletxt)
        print("saved temp files")
        idf_temp = eppy.openidf(idf_temp_file, epw=wfile_temp_file)
        fullresult = runandget.anon_runandget(idf_temp, getdict)
        print(fullresult)
    return fullresult

while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Received request:")
    
    #  Do some 'work'
    idftxt, wfiletxt, getdict = message
    fullresult = zeppy_runandget(idftxt, wfiletxt, getdict)

    #  Send reply back to client
    socket.send_pyobj(fullresult)