from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from s3dump.utils.common._collections_compat import Mapping, Set
from s3dump.utils.common.collections import is_sequence
from s3dump.utils.context_objects import CLIArgs, GlobalCLIArgs


__all__ = ('CLIARGS')


CLIARGS = CLIArgs({})


def _init_global_context(cli_args):
    """Initialize the global context objects."""

    global CLIARGS
    CLIARGS = GlobalCLIArgs.from_options(cli_args)


def cliargs_deferred_get(key, default=None, shallowcopy=False):
    """Closure over getting a key from CLIARGS with shallow copy functionality."""

    def inner():
        value = CLIARGS.get(key, default=default)
        if not shallowcopy:
            return value
        elif is_sequence(value):
            return value[:]
        elif isinstance(value, (Mapping, Set)):
            return value.copy()
        return value

    return inner
