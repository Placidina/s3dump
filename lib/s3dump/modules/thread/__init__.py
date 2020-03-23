from __future__ import absolute_import, division, print_function
__metaclass__ = type

from threading import Lock, Thread as T


class Thread(T):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        T.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def wait(self, *args):
        T.join(self, *args)
        return self._return
