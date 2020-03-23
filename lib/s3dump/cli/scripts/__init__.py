#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
__requires__ = ['s3dump']


import os
import sys
import traceback

from s3dump import context
from s3dump.errors import S3DumpError, S3DumpOptionsError, S3DumpParserError
from s3dump.utils._text import to_text


# Used for determining if the system is running a new enough python version
# and should only restrict on our documented minimum versions
_PY3_MIN = sys.version_info[:2] >= (3, 5)
_PY2_MIN = (2, 6) <= sys.version_info[:2] < (3,)
_PY_MIN = _PY3_MIN or _PY2_MIN
if not _PY_MIN:
    raise SystemExit(
        "ERROR: Requires a minimum of Python2 version 2.6 or Python3 version 3.5. Current version: %s" % ''.join(sys.version.splitlines()))


class LastResort(object):
    def display(self, msg, log_only=None):
        print(msg, file=sys.stderr)

    def error(self, msg, wrap_text=None):
        print(msg, file=sys.stderr)


if __name__ == '__main__':
    display = LastResort()

    try:
        import s3dump.constants as C
        from s3dump.utils.display import Display
    except S3DumpOptionsError as e:
        display.error(to_text(e))
        sys.exit(5)

    cli = None
    me = os.path.basename(sys.argv[0])

    try:
        display = Display()

        sub = None
        target = me.split('-')
        if target[-1][0].isdigit():
            target = target[:-1]

        if len(target) > 1:
            sub = target[1]
            myclass = "%sCLI" % sub.capitalize()
        elif target[0] == 's3dump':
            sub = 's3dump'
            myclass = 'S3Dump'
        else:
            raise S3DumpError("Unknown S3Dump alias: %s" % me)

        try:
            mycli = getattr(
                __import__("s3dump.cli.%s" % sub, fromlist=[myclass]), myclass)
        except ImportError as e:
            if 'msg' in dir(e):
                msg = e.msg
            else:
                msg = e.message

            if msg.endswith(' %s' % sub):
                raise S3DumpError(
                    "S3Dump sub-program not implemented: %s" % me)
            else:
                raise

        try:
            args = [to_text(a, errors='surrogate_or_strict') for a in sys.argv]
        except UnicodeError:
            display.error(
                "Command line args are not in utf-8, unable to continue. S3Dump currently only understands utf-8")
            display.display(
                u"The full traceback was:\n\n%s" % to_text(traceback.format_exc()))
            exit_code = 6
        else:
            cli = mycli(args)
            exit_code = cli.run()
    except S3DumpOptionsError as e:
        cli.parser.print_help()
        display.error(to_text(e))
        exit_code = 5
    except S3DumpParserError as e:
        display.error(to_text(e))
        exit_code = 4
    except S3DumpError as e:
        display.error(to_text(e))
        exit_code = 1
    except KeyboardInterrupt:
        display.error("User interrupted execution")
        exit_code = 99
    except Exception as e:
        if C.DEFAULT_DEBUG:
            raise
        have_cli_options = bool(context.CLIARGS)
        display.error(
            "Unexpected Exception, this is probably a bot bug: %s" % to_text(e))

        if not have_cli_options or have_cli_options and context.CLIARGS['verbosity'] > 2:
            log_only = False

            if hasattr(e, 'orig_exc'):
                display.vvv("\nexception type: %s" % to_text(type(e.orig_exc)))
                why = to_text(e.orig_exc)

                if to_text(e) != why:
                    display.vvv("\noriginal msg: %s" % why)
        else:
            display.display("to see the full traceback, use -vvv")
            log_only = True

        display.display(
            u"the full traceback was:\n\n%s" % to_text(traceback.format_exc()), log_only=log_only)
        exit_code = 250

    sys.exit(exit_code)
