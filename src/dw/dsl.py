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

from abc import ABC, abstractmethod
import io as _io
import logging as _logging

_LOGGER: _logging.Logger = _logging.getLogger(__name__)

_DEBUG: bool = True


class AbstractIterableMonadicFunction(ABC):

    @abstractmethod
    def __call__(self, iterable: _Iterable) -> IterableMonad:
        pass


class IterableMonad(object):

    def __init__(self, iterable: _Iterable[object] = [], name="IterableMonad"):
        _LOGGER.debug("Creating %s: %s with iterable %s", type(self).__name__, name, type(iterable))
        self.__name__ = name
        self.name: str = name
        self.iterable: _Iterable = iterable

    ################################################
    # implements monad
    def bind(self, mf: _Callable) -> IterableMonad:
        mf_name:str = mf.__name__ if getattr(mf, "__name__", None) else \
                      mf.__class__.__name__ if getattr(mf, "__class__", None) else \
                      "mf"
        _LOGGER.debug("Binding from IM: %s to MF: %s", self.name, mf_name)
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
    def redirect_to(self, sink: object) -> object:
        _LOGGER.debug("Redirecting from %s to %s", self.name, type(sink).__name__)
        other = self.bind(tee(sink))
        # consume
        for _ in other:
            pass
        return sink

    __gt__ = redirect_to  # range(5) | sort() > []

    def appending_redirect_to(self, sink: object) -> object:
        _LOGGER.info("Redirecting with append mode from %s to %s", self.name, type(sink).__name__)
        other = self.bind(tee(sink, append=True))
        # consume
        for _ in other:
            pass
        return sink

    __rshift__ = appending_redirect_to  # (range(5) | sort() ) >> "filename". because >> is stronger than |.


################################################################################
# Class that is superposition of Monad and MonadicFunction.
# If it is called as function, it behaves like Monadic Function and returns Monad
# If it is called as a argument of __ror__, it behaves like Monad
class FlippableIterableMonadicFunction(AbstractIterableMonadicFunction):

    def __init__(self, monadic_function: _Callable):
        self._mf: _Callable = monadic_function

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return self._mf(iterable)

    def __ror__(self, iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable, name=type(iterable).__name__).bind(self._mf)


################################################################################
#  Tee


def tee(sink: object, append: bool = False) -> _Callable:

    def monadic_func(iterable: _Iterable) -> _Iterable[object]:

        if isinstance(sink, _Sequence):
            if not append:
                sink.clear()
            for obj in iterable:
                sink.append(obj)
                yield obj
        else:
            raise ValueError(f"sink=={sink} is not instance of either io, Sequence, or Set")

    return monadic_func
