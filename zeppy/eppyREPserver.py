# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""server gets a text file of idf and wfile"""

import time
import zmq
from zeppy import z_runners 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()
    print("Received request:")
    
    #  Do some 'work'
    idftxt, wfiletxt, getdict = message
    fullresult = z_runners.zeppy_runandget(idftxt, wfiletxt, getdict)

    #  Send reply back to client
    socket.send_pyobj(fullresult)