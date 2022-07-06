import zmq
import time
import numpy as np
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client

    # generate random coordinates for the plane
    x = np.random.randint(0, 100)
    y = np.random.randint(0, 100)

    socket.send(b"{} {}".format(x, y))
