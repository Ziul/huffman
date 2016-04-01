# -*- coding: utf-8 -*-
from bitarray import bitarray
import re
import string
import struct
from bitargs import _parser
# xxd  -b file.txt

global _options
global _args


class Bitset(bitarray):
    memory = None
    verbose = True

    def __init__(self, **arg):
        super(Bitset, self).__init__(**arg)
        self.code = {}
        if 'name' in arg.keys():
            self.name = arg['name']
        else:
            self.name = 'file.bin'

        # encode ASCII table
        for x in string.printable:
            self.code[x] = bitarray(bin(ord(x)).split('0b')[1].rjust(8, '0'))
        # self.checker = re.compile(ur'([^01]+)')

    def push(self, arg):
        if (arg[0:2] == '0b') and len(arg) > 2:
            try:
                super(Bitset, self).extend(arg.split('0b')[1])
                return
            except Exception:
                pass
        a = bitarray()
        a.encode(self.code, arg)

        super(Bitset, self).extend(a)

    def to_file(self):
        if (len(self) % 8):
            if self.verbose:
                print('flushed with %d' % (len(self) % 8))
            self.fill()
        bits = self.__str__()
        # if self.verbose:
        #     print(">>: ", bits, '(', len(bits), ')')
        with open(self.name, "wb") as f:
            for i in self.chunks(bits, 8):
                # int_value = int(i[::-1], base=2)
                # bin_array = struct.pack('i', int_value)
                int_value = int(i, base=2)
                bin_array = struct.pack('B', int_value)
                f.write(bin_array)

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def flush(self):
        self.fill()
        self.memory = memoryview(self)

    def pack(self):
        size = 8 - (len(self) % 8)
        for i in range(size):
            self.insert(0, False)

    def __str__(self):
        output = super(Bitset, self).__str__()
        output = output.replace('bitarray(\'', '')
        output = output.replace('\')', '')
        return output


def main():

    (_options, _args) = _parser.parse_args()
    a = Bitset()
    a.name = _options.filename
    a.verbose = _options.verbose
    if not _args:
        _parser.print_help()
        return
    a.extend(_args[0])

    if _options.verbose:
        print('<<: ', a, '(', len(a), ')')
    a.to_file()


def test():
    pass

if __name__ == '__main__':
    main()
