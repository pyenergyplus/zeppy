vent
ventipc
# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")
# Socket with direct access to the sink: used to synchronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")


worker
# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")
# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

sink
# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")


5557
5558

PUB SUB
PUB
killipc
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

PUB
resultipc
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

SUB
killicp
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

SUB
resultipc
resultipcsocket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

5555
5556