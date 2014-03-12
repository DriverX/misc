import os
import sys
from tornado.ioloop import IOLoop
import socket
import signal
from functools import partial


def sock_handler(sock, fd, events):
    print fd, events, sock.recv(1024)


def child_init(sock):
    sock.setblocking(False)

    ioloop = IOLoop.instance()
    ioloop.add_handler(sock.fileno(), partial(sock_handler, sock), ioloop.READ)
    ioloop.start()


def main():
    sock_send, sock_recv = socket.socketpair()

    child_pid = os.fork()
    if not child_pid:
        child_init(sock_recv)
        return

    while True:
        line = sys.stdin.readline()
        sock_send.send(line)

    os.kill(child_pid, signal.CTRL_C_EVENT)
    sys.exit()


if __name__ == "__main__":
    main()
