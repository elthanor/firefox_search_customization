#!/usr/bin/env python3

import lz4
import sys

from argparse import ArgumentParser


class MozLz4aError(Exception):
    pass


class InvalidHeader(MozLz4aError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def decompress(file_obj):
    if file_obj.read(4) != b"mozLz40\0":
        raise InvalidHeader("Invalid magic number")

    return lz4.decompress(file_obj.read())


def compress(file_obj):
    compressed = lz4.compress(file_obj.read())
    return b"mozLz40\0" + compressed


if __name__ == "__main__":
    argparser = ArgumentParser(description="MozLz4a compression/decompression utility")
    argparser.add_argument(
        "-d", "--decompress", "--uncompress",
        action="store_true",
        help="Decompress the input file instead of compressing it."
    )
    argparser.add_argument(
        "in_file",
        help="Path to input file."
    )
    argparser.add_argument(
        "out_file",
        help="Path to output file."
    )

    parsed_args = argparser.parse_args()

    try:
        in_file = open(parsed_args.in_file, "rb")
    except IOError as e:
        print("Could not open input file `%s' for reading: %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(2)

    try:
        out_file = open(parsed_args.out_file, "wb")
    except IOError as e:
        print("Could not open output file `%s' for writing: %s" % (parsed_args.out_file, e), file=sys.stderr)
        sys.exit(3)

    try:
        if parsed_args.decompress:
            data = decompress(in_file)
        else:
            data = compress(in_file)
    except Exception as e:
        print("Could not compress/decompress file `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(4)

    try:
        out_file.write(data)
    except IOError as e:
        print("Could not write to output file `%s': %s" % (parsed_args.out_file, e), file=sys.stderr)
        sys.exit(5)
    finally:
        out_file.close()
