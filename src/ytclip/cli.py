import os
import re
from urllib.parse import urlparse
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from sys import stdout
from typing import BinaryIO

__TIME_REGEX = re.compile(r'^(?:\d+:)?(?:[0-5]?[0-9]:)?(?:[0-5]?[0-9])(?:\.\d+)?$')

def __url_type(_arg: str) -> str:
    arg = _arg.strip()
    try:
        url = urlparse(arg)
    except:
        raise ArgumentTypeError(f"Input URL {arg} is not parseable.")
    else:
        return arg

def __time_type(_arg: str) -> str:
    arg = _arg.strip()
    if __TIME_REGEX.fullmatch(arg):
        return arg
    raise ArgumentTypeError(f"Invalid time string \"{arg}\"")

def __writable_path_type(_arg: str) -> Path | BinaryIO:
    '''A context manager to handle opening a binary writable stream.

    :param arg: Path-like argument. 
    :type arg: str
    :raises ArgumentTypeError: The path-like that the argument points to exists but is not a file.
    :raises ArgumentTypeError: The parent directory of the path-like that the argument points to is not writable.
    :raises ArgumentTypeError: The path-like that the argument points to is not writable.
    :rtype: Generator[BinaryIO, None, None]
    '''
    arg = _arg.strip()
    if arg == "-":
        return stdout.buffer
    else:
        path = Path(arg).resolve()
        if not os.access(path.parent, os.W_OK):
            raise ArgumentTypeError(f'Parent directory of output path "{path}" is not writable.')
        if path.exists():
            if not path.is_file():
                raise ArgumentTypeError(f'Output path "{path}" exists but is not a file.')
            if not os.access(path, os.W_OK):
                raise ArgumentTypeError(f'Output path "{path}" is not writable.')
        return path

def __get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Download via yt-dlp and then clip and remux in one command.")
    parser.add_argument('-o', '--output', 
                        type=__writable_path_type, 
                        dest="output",
                        default="-",
                        help="Path to output file to.")
    parser.add_argument("-s", "--start",
                        type=__time_type,
                        dest="start",
                        default=None,
                        help="Start time for clipping.")
    parser.add_argument("-t", "--to",
                        type=__time_type,
                        dest="end",
                        default=None,
                        help="End time for clipping.")
    parser.add_argument("url",
                        type=__url_type,
                        help="URL to downloadable video.")
    return parser
    
def parse_args() -> Namespace:
    parser = __get_parser()
    return parser.parse_args()