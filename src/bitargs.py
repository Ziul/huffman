import optparse


_parser = optparse.OptionParser(
    usage="""%prog BITARRAY [OPTIONS]
Examples:
Write '01010101011011010' into `file.bin`:
    ~ $ writebits 01010101011011010
Write '01010101011011010' into `teste.txt`:
    ~ $ writebits 01010101011011010 -f teste.txt
        """,
    description="Write a array of bits into a file",
)

# quiet options
_parser.add_option("-q", "--quiet",
                   dest="verbose",
                   action="store_false",
                   help="suppress non error messages",
                   default=True
                   )

_parser.add_option("-f", "--filename",
                   dest="filename",
                   type='string',
                   help="Name of the file",
                   default='file.bin'
                   )
