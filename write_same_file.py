from __future__ import division
import os
import sys
import string
import random
import time
from binascii import hexlify
import multiprocessing as mp


def _reseed_random():
    if 'random' not in sys.modules:
        return
    import random
    # If os.urandom is available, this method does the same thing as
    # random.seed (at least as of python 2.6).  If os.urandom is not
    # available, we mix in the pid in addition to a timestamp.
    try:
        seed = long(hexlify(os.urandom(16)), 16) 
    except NotImplementedError:
        seed = int(time.time() * 1000) ^ os.getpid()
    random.seed(seed)


def child_init(f, word, lock):
    _reseed_random()

    s = word * 5000
    while True:
        # with lock:
        #     f.write(s)
        f.write(s)
        f.flush()
        time.sleep(int(random.uniform(0.1, 0.5) * 100) / 100)
    

def main():
    words = string.ascii_lowercase
    open("same_file.txt", "w").close()
    f = open("same_file.txt", "a", 0)
    lock = mp.Lock()
    for i in xrange(24):
        child_pid = os.fork()
        if not child_pid:
            # f = open("same_file.txt", "a")
            child_init(f, words[i], lock)
            return

    os.wait()
    sys.exit()


if __name__ == "__main__":
    main()
