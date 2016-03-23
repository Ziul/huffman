import sys
import ipdb
import operator
import Queue as queue
from huffargs import _parser
# xxd  -b file.txt


class HuffmanNode(object):
    code = {}

    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right
        self.root = root

    def children(self):
        return (self.left, self.right)

    def precoder(self, path=None):
        if path is None:
            path = []
        if self.left is not None:
            if isinstance(self.left[1], HuffmanNode):
                self.left[1].precoder(path + [0])
            else:
                # print(self.left, ''.join(str(x) for x in path + [0]))
                self.code[self.left[1]] = ''.join(
                    str(x) for x in path + [0])
        if self.right is not None:
            if isinstance(self.right[1], HuffmanNode):
                self.right[1].precoder(path + [1])
            else:
                # print(self.right, ''.join(str(x) for x in path + [1]))
                self.code[self.right[1]] = ''.join(
                    str(x) for x in path + [1])


def encode(frequencies):
    p = queue.PriorityQueue()
    for item in frequencies:
        p.put(item)

    # invariant that order is ascending in the priority queue
    # p.size() gives list of elements
    while p.qsize() > 1:
        left, right = p.get(), p.get()
        node = HuffmanNode(left, right)
        p.put((left[0] + right[0], node))
    return p.get()


def build_probability(file):
    freq = {}
    with open(file, "r") as f:
        data = f.read()
        for i in data:
            if i in freq.keys():
                freq[i] += 1
            else:
                freq[i] = 1.0
        for k in freq:
            freq[k] = freq[k] / len(data)

    # return freq
    sorted_values = []
    for i in sorted(freq.items(), key=operator.itemgetter(1), reverse=True):
        sorted_values.append((i[1], i[0]))
    return sorted_values


def main():
    (_options, _args) = _parser.parse_args()
    if not _options.filename:
        if _args:
            _options.filename = _args[0]
        else:
            _parser.print_help()
            return
    freq = build_probability(_options.filename)
    node = encode(freq)
    node[1].precoder()
    print node[1].code

if __name__ == '__main__':
    main()
