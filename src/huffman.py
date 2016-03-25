# -*- coding: utf-8 -*-

"""
Huffman algorithm.

Used to encode/decode files, as
create table from a file.
"""

from heapq import heappush, heappop, heapify
from collections import defaultdict
from huffargs import _parser
from writebits import Bitset


class HuffmanCompactor(object):
    """docstring for Huffman Compactor."""

    def __init__(self, filename):
        """Initialize the object."""
        super(HuffmanCompactor, self).__init__()
        self.filename = filename
        self.txt = open(self.filename, "r").read()
        self.symb2freq = defaultdict(int)
        for ch in self.txt:
            self.symb2freq[ch] += 1
        if not len(self.symb2freq):
            raise IndexError('Input is empty, no magic here...')
        self.bitarray = Bitset()
        self.bitarray.name = filename.split('/')[-1] + '.huff'
        self.dict_table = {}

    def build_table(self):
        """Create the Huffman table of the given dict mapping symbols."""
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
            f.write(str(self.dict_table))
        self.bitarray.to_file()

    def __str__(self):
        """Format the output preatty."""
        out = "Symbol       Weight\tHuffman Code\n"
        for p in self.table:
            # print "%s\t\t%s\t%s" % ([p[0]], symb2freq[p[0]], p[1])
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
    huff = HuffmanCompactor(_options.filename)
    huff.write()

if __name__ == '__main__':
    main()
