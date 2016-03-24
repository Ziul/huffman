from heapq import heappush, heappop, heapify
from collections import defaultdict
from huffargs import _parser


def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def main():
    (_options, _args) = _parser.parse_args()
    if not _options.filename:
        if _args:
            _options.filename = _args[0]
        else:
            _parser.print_help()
            return
    txt = open(_options.filename, "r").read()

    symb2freq = defaultdict(int)
    for ch in txt:
        symb2freq[ch] += 1
    # in Python 3.1+:
    # symb2freq = collections.Counter(txt)
    huff = encode(symb2freq)
    print "Symbol       Weight\tHuffman Code"
    for p in huff:
        # print "%s\t\t%s\t%s" % ([p[0]], symb2freq[p[0]], p[1])
        print '{}'.format([p[0]]).ljust(13),
        print '{}\t'.format(symb2freq[p[0]]).rjust(5),
        print '{}'.format(p[1]).ljust(20)
if __name__ == '__main__':
    main()
