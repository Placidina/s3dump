from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import operator
import argparse
import sys

import s3dump
from s3dump import constants as C
from s3dump.utils._text import to_native
from s3dump.release import __version__


class SortingHelpFormatter(argparse.HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=operator.attrgetter('option_strings'))
        super(SortingHelpFormatter, self).add_arguments(actions)


class Version(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        s3dump_version = to_native(version(getattr(parser, 'prog')))
        print(s3dump_version)
        parser.exit()


def version(prog=None):
    """S3Dump version."""

    if prog:
        result = ' '.join((prog, __version__))
    else:
        result = __version__

    result = result + \
        "\n  Python module location = %s" % ':'.join(s3dump.__path__)
    result = result + "\n  Executable location = %s" % sys.argv[0]
    result = result + \
        "\n  Python version = %s" % ''.join(sys.version.splitlines())

    return result


def create_base_parser(prog, usage="", desc=None, epilog=None):
    """Create an options parser for all scripts."""

    version_help = "Show program's version number, config file location, configured module search path, module location, executable location and exit"

    parser = argparse.ArgumentParser(
        prog=prog, formatter_class=SortingHelpFormatter, epilog=epilog, description=desc, conflict_handler='resolve')

    parser.add_argument(
        '--version', action=Version, nargs=0, help=version_help)

    add_verbosity_options(parser)
    add_debug_options(parser)

    return parser


def add_verbosity_options(parser):
    """Add options for verbosity."""

    parser.add_argument(
        '-v', '--verbose', dest='verbosity', default=C.DEFAULT_VERBOSITY, action='count', help="Verbose mode (-vvv for more)")


def add_debug_options(parser):
    """Add options for debug."""

    parser.add_argument(
        '--debug', dest='debugging', default=C.DEFAULT_DEBUG, action='store_true', help="Enable debugging mode")
