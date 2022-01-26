
from argparse import _SubParsersAction

def get_version():
    return "v0.1.15"

def print_version(*_args, **_kwargs):
    print(get_version())

def get_version_parser(subParsers: _SubParsersAction):
    version_parser = subParsers.add_parser('version', help="Get version")
    version_parser.set_defaults(func=print_version)
    return version_parser
