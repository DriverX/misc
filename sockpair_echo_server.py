import os
import sys
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import stack_context
import socket
import signal
from functools import partial

task_id = None


def sock_handler(sock, fd, events):
    print fd, events, sock.recv(1024)
    if task_id % 2 == 0:
        sock.close()


def child_init(id, sock):
    global task_id
    task_id = id

    sock.setblocking(False)

    ioloop = IOLoop.instance()
    ioloop.add_handler(sock.fileno(), partial(sock_handler, sock), ioloop.READ)
    ioloop.start()


def master_check_send(socks, fd, events):
    line = sys.stdin.readline()
    for i, sock in enumerate(socks):
        try:
            sock.send(line)
        except Exception, e:
            print i, e


def main():
    socks = []

    for i in xrange(6):
        sock_send, sock_recv = socket.socketpair()
        child_pid = os.fork()
        if not child_pid:
            socks = None
            child_init(i, sock_recv)
            return
        socks.append(sock_send)
    
    ioloop = IOLoop.instance()
    cb = stack_context.wrap(partial(master_check_send, socks))
    ioloop.add_handler(sys.stdin.fileno(), cb, ioloop.READ)
    
    def stop(sig, frame):
        ioloop.add_callback(ioloop.stop)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    ioloop.start()

    sys.exit()


if __name__ == "__main__":
    main()
