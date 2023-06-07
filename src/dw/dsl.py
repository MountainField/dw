# -*- coding: utf-8 -*-

# =================================================================
# dw
#
# Copyright (c) 2022 Takahide Nogayama
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# =================================================================

# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations as _annotations

from collections.abc import Iterable as _Iterable
from collections.abc import Iterator as _Iterator
from collections.abc import Callable as _Callable
from collections.abc import Sequence as _Sequence

import io as _io
import logging as _logging

_LOGGER: _logging.Logger = _logging.getLogger(__name__)

_DEBUG: bool = True


class IterableMonad(object):

    def __init__(self, iterable: _Iterable[object] = [], name="IterableMonad"):
        _LOGGER.debug("Creating %s: %s with iterable %s", type(self).__name__, name, type(iterable))
        self.__name__ = name
        self.name: str = name
        self.iterable: _Iterable = iterable

    ################################################
    # implements monad
    def bind(self, mf: _Callable) -> IterableMonad:
        _LOGGER.debug("Binding from IM: %s to MF: %s", self.name, mf.__name__)
        new_im: IterableMonad = mf(self.iterable)
        return new_im

    __or__ = bind

    ################################################
    # implements Iterable
    def __iter__(self) -> _Iterator:
        # return self.iterable
        return iter(self.iterable)

    ################################################
    # implements human readable representation
    def __str__(self) -> str:
        sio: _io.StringIO = _io.StringIO()
        for obj in self.iterable:
            sio.write(str(obj))
            sio.write("\n")
        return sio.getvalue()

    __repr__ = __str__

    ################################################
    # implements redirection
    def redirect_to(self, sink) -> object:
        _LOGGER.debug("Redirecting from %s to %s", self.name, type(sink).__name__)
        other = self.bind(tee(sink))
        # consume
        for _ in other:
            pass
        return sink

    __gt__ = redirect_to  # range(5) | sort() > []


def tee(sink: object) -> _Callable:

    def monadic_func(iterable: _Iterable) -> _Iterable[object]:

        if isinstance(sink, _Sequence):
            for obj in iterable:
                sink.append(obj)
                yield obj
        else:
            raise ValueError(f"sink=={sink} is not instance of either io, Sequence, or Set")

    return monadic_func
