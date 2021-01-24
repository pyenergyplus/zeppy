===========================================
Running eppy in a REQ-REP pattern in zeromq
===========================================

How it works
============

The REQ-REP pattern is a simple messaging pattern in ZeroMQ. It works this way:

- The client sends a message to the server
- the server replies to the client

Running eppy and E+ using this pattern looks like this;

- read the idf file (``idftxt``), the weather file (``wfiletxt``) as text files
- make a ``getdict`` dictionary. This is a definition of what data you want back from the simulation.
    - Maybe I want the 3rd column from the csv file and the second table from the html table file
    - more on this later
- The client sends the following to the server
    - an id <to keep track fo your runs>
    - ``idftxt``
    - ``wfiletxt``
    - ``getdict``
- The server will run the `idf` and return the data defined in ``getdict``

Thats it !

On ``getdict``
==============

Read about ``getdict`` in `Run and get results <https://witheppy.readthedocs.io/en/latest/runandget.html>`_ This is the documentation of code in the respository https://github.com/pyenergyplus/witheppy


Try it out
==========

Running everything locally
--------------------------

- run ``eppyREQclient.py`` in one terminal
- run ``eppyREPserver.py`` on another terminal
- You can start them in any order (server first or client first)

Running the server on a remote computer
---------------------------------------

- get the ip address of the computer you are using as a server. Let us call it SERVER_IP.
    - the server computer can be on the cloud, as long as the IP is accessible from the client.
    - Or the server can be simply another computer
- run ``eppyREPserver.py`` on the server computer
- edit ``eppyREPserver.py`` by changing the line ``socket.connect("tcp://localhost:5555")`` to ``socket.connect("tcp://SERVER_IP:5555")``
- run ``eppyREQclient.py`` on the client computer