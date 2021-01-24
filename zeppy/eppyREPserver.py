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

try:
    import zeppy.z_runners as z_runners
except ModuleNotFoundError as e:
    import z_runners

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def main():
    while True:
        #  Wait for next request from client
        message = socket.recv_pyobj()
        print("Received request:")

        #  Do some 'work'
        run_id, (idftxt, wfiletxt, getdict) = message
        fullresult = z_runners.zeppy_runandget(idftxt, wfiletxt, getdict)

        #  Send reply back to client
        message = run_id, fullresult
        socket.send_pyobj(message)


if __name__ == "__main__":
    main()
