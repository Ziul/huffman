# -*- coding: utf-8 -*-

"""
Huffman algorithm.

Used to encode/decode files, as
create table from a file.
"""

import json
from heapq import heappush, heappop, heapify
from collections import defaultdict
from huffargs import _parser
from writebits import Bitset
from bitarray import bitarray


class HuffmanCompactor(object):
    """docstring for Huffman Compactor."""

    def __init__(self, filename, verbose=True, mode='bin'):
        """Initialize the object."""
        super(HuffmanCompactor, self).__init__()
        self.filename = filename
        self.mode = mode
        self.verbose = verbose
        self.bitarray = Bitset()
        self.bitarray.verbose = self.verbose
        self.dict_table = {}

    def encoding(self):
        self.txt = open(self.filename, "rb",).read()

        self.symb2freq = defaultdict(int)
        self.symb2freq[256] = 0
        for ch in self.txt:
            self.symb2freq[ch] += 1
        if not len(self.symb2freq):
            raise IndexError('Input is empty, no magic here...')
        self.bitarray.name = self.filename.split('/')[-1] + '.huff'

    def build_table(self):
        """Create the Huffman table of the given dict mapping symbols."""
        self.encoding()
        heap = [[wt, [sym, ""]] for sym, wt in self.symb2freq.items()]
        heapify(heap)
        while len(heap) > 1:
            lo = heappop(heap)
            hi = heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        self.table = sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
        for item in self.table:
            self.dict_table[item[0]] = item[1]
        return self.table

    def build_array(self):
        if not self.dict_table:
            self.build_table()
        for ch in self.txt:
            self.bitarray.extend(self.dict_table[ch])

    def write(self):
        if not len(self.bitarray):
            self.build_array()
        with open(self.filename.split('/')[-1] + '.table', "w") as f:
            json.dump(self.dict_table, f)
        self.bitarray.extend(self.dict_table[256])
        self.bitarray.to_file()

    def read(self):
        table_file = self.filename.split('.')[:-1]
        table_file = '.'.join(table_file) + '.table'

        with open(table_file) as json_file:
            self.dict_table = json.load(json_file)

        with open(table_file.replace('.table', '.huff'), 'rb') as file:
            self.bitarray.fromfile(file)
            self.bitarray = self.bitarray.to01()

        decoded = ''
        data = ''

        while decoded != '256':
            for i in range(1, len(self.dict_table['256']) + 1):
                sym = self.bitarray[:i]
                if sym in self.dict_table.values():
                    decoded = list(self.dict_table.keys()
                                   )[list(self.dict_table.values()).index(sym)]
                    if decoded == '256':
                        return data
                    data += chr(int(decoded))
                    self.bitarray = self.bitarray[i:]

        # '01' in a.values() # check presence
        # list(a.keys())[list(a.values()).index(0)] # get symb

    def decode(self):
        data = self.read()
        filename = self.filename.split('.')[:-1]
        filename = '.'.join(filename)
        with open('decoded_' + filename, 'w') as file:
            file.write(data)
        if self.verbose:
            import os
            os.system('diff {} {}'.format(filename, 'decoded_' + filename))

    def __str__(self):
        """Format the output preatty."""
        out = "Symbol       Weight\tHuffman Code\n"
        for p in self.table:
            out += '\r{}'.format([p[0]]).ljust(13)
            out += '{}\t'.format(self.symb2freq[p[0]]).rjust(5)
            out += '{}\n'.format(p[1]).ljust(20)
        return out


def main():
    """Main call."""
    (_options, _args) = _parser.parse_args()
    if not _options.filename:
        if _args:
            _options.filename = _args[0]
        else:
            _parser.print_help()
            return
    huff = HuffmanCompactor(_options.filename, _options.verbose, _options.mode)
    if _options.encode:
        huff.write()
    else:
        huff.decode()

if __name__ == '__main__':
    main()
