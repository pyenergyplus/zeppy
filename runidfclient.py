#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
"""server for run the eppy.modelmaker.IDF and wfile=filepath"""

import zmq
import eppy
import pprint
pp = pprint.PrettyPrinter()

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send request
idfname = "./idffolder/1ZoneUncontrolled.idf"
wfile = "./idffolder/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
wfiletxt = open(wfile, 'r').read()
idf = eppy.openidf(idfname, epw=wfile)

getdict = dict(
    end_file=dict(whichfile="end", entirefile=True),
)
getdict = dict(
    HTML_file=dict(whichfile="htm", tableindex=0, table=True),
)
getdict = dict(
    twocells=dict(
        whichfile="htm",
        # tableindex=0,  # or tablename
        tablename="Site and Source Energy",  # tableindex takes priority if both given
        cells=[[-2, 1], [-2, -2]],  # will return 2 cells
    ),
    HTML_file=dict(whichfile="htm", tableindex=0, table=True)
)

print("sending message")
socket.send_pyobj((idf, wfiletxt, getdict))

#  Get the reply.
message = socket.recv_pyobj()
print('-' *8)
print("results are:")
pp.pprint(message)
# print("Received reply %s [ %s ]" % (request, message))