from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
from abc import ABCMeta, abstractmethod

from s3dump import context
from s3dump.cli import arguments
from s3dump.utils.six import with_metaclass
from s3dump.utils._text import to_text
from s3dump.utils.display import Display

try:
    import argcomplete
    HAS_ARGCOMPLETE = True
except ImportError:
    HAS_ARGCOMPLETE = False


display = Display()


class CLI(with_metaclass(ABCMeta, object)):
    """Code behind bin/* programs."""

    def __init__(self, args, callback=None):
        """Base init method for all command line programs."""

        if not args:
            raise ValueError("A non-empty list for args is required")

        self.args = args
        self.parser = None
        self.callback = callback

    @abstractmethod
    def run(self):
        """Run the bin/* command."""

        self.parse()
        display.vv(to_text(arguments.version(self.parser.prog)))

    @abstractmethod
    def init_parser(self, usage="", desc=None, epilog=None):
        """Create an options parser for most scripts."""

        self.parser = arguments.create_base_parser(os.path.basename(
            self.args[0]), usage=usage, desc=desc, epilog=epilog, )

    @abstractmethod
    def post_process_args(self, options):
        """Process the command line args."""

        return options

    def parse(self):
        """Parse the command line args."""

        self.init_parser()

        if HAS_ARGCOMPLETE:
            argcomplete.autocomplete(self.parser)

        options = self.parser.parse_args(self.args[1:])
        options = self.post_process_args(options)
        context._init_global_context(options)
