import sys
import ipdb
import operator
from bitargs import _parser
# xxd  -b file.txt

global _options
global _args

table = {}


def build_probability(file):
    with open(file, "r") as f:
        data = f.read()
        for i in data:
            if i in table.keys():
                table[i] += 1
            else:
                table[i] = 1


def main():
    (_options, _args) = _parser.parse_args()
    if not _options.filename:
        if _args:
            _options.filename = _args[0]
    else:
        return
    build_probability(sys.argv[1])
    print table
    sorted_x = sorted(table.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_x

if __name__ == '__main__':
    main()
