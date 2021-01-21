#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

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
    print("Received request:",  message)

    #  Do some 'work'
    idfname, wfile, getdict = message
    idf = eppy.openidf(idfname, epw=wfile)
    fullresult = runandget.anon_runandget(idf, getdict)
    print(fullresult)

    #  Send reply back to client
    socket.send_pyobj(fullresult)