from itertools import takewhile


def main():
    start_byte = 0
    read_byte = 10
    with open("same_file.txt") as f:
        while True:
            entry = f.read(read_byte)
            if not entry:
                break
            fc = entry[0]
            res = filter(lambda c: c != fc, entry)
            if res:
                print "Bad entry found. slice-%d, char-%s, entry-%s" % (
                    start_byte, fc, entry)
                return
            start_byte += read_byte
    print "Bad entries not found"


if __name__ == "__main__":
    main()
