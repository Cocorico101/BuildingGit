import argparse
import configparser
from datetime import datetime
from fnmatch import fnmatch
import hashlib
from math import ceil
import importlib
import os
import re
import sys
import zlib
try:
    import grp, pwd
except ModuleNotFoundError:
    pass


# Add subparsers because we need it to be git COMMAND
COMMAND_MODULES = [
    "commands.init",
    "commands.cat-file",
    "commands.hash-object",
    "commands.log",
    "commands.ls-tree"
    # "commands.commit"
]

def main(argv=sys.argv[1:]):
    # Top level parser
    argparser = argparse.ArgumentParser(description="The stupidest content tracker")
    # Register subparsers to the subparser table
    argsubparsers = argparser.add_subparsers(title="Commands List", dest="command", required=True)
    for module in COMMAND_MODULES:
        mod = importlib.import_module(module)
        mod.register(argsubparsers)
    
    # Parse the commands and invoke the registered handler
    args = argparser.parse_args(argv)
    args.func(args)
