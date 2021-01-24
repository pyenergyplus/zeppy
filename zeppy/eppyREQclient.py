# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""client sends a text file of idf and wfile"""

import zmq
import eppy
import z_runners 

import pprint
pp = pprint.PrettyPrinter()

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
# socket.connect("tcp://192.168.42.144:5555")

# send request
idfname = "./idffolder/1ZoneUncontrolled.idf"
idfname = "/Applications/EnergyPlus-9-1-0/ExampleFiles/1ZoneEvapCooler.idf"
wfile = "./idffolder/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"

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
idftxt, wfiletxt = z_runners.to_zeppy_runandget(idfname, wfile)
socket.send_pyobj((idftxt, wfiletxt, getdict))

#  Get the reply.
message = socket.recv_pyobj()
print('-' *8)
print("results are:")
pp.pprint(message)
# print("Received reply %s [ %s ]" % (request, message))
