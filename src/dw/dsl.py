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
from collections.abc import Set as _Set

from abc import ABC, abstractmethod
import io as _io
import logging as _logging

_LOGGER: _logging.Logger = _logging.getLogger(__name__)

_DEBUG: bool = True


def consume(iterable: _Iterable):
    for _ in iterable:
        pass


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
    def bind(self, imf: _Callable) -> IterableMonad:
        imf_name:str = imf.__name__ if getattr(imf, "__name__", None) else \
                      imf.__class__.__name__ if getattr(imf, "__class__", None) else \
                      "imf"
        _LOGGER.debug("Binding from IM: %s to IMF: %s", self.name, imf_name)
        new_im: IterableMonad = imf(self.iterable)
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
# If it is called as a argument of __ror__, it wraps iterable and returns Monad
class FlippableIterableMonadicFunction(AbstractIterableMonadicFunction):

    def __init__(self, iterable_monadic_function: _Callable):
        self._iterable_monadic_function: _Callable = iterable_monadic_function

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return self._iterable_monadic_function(iterable)

    def __ror__(self, iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable, name=type(iterable).__name__).bind(self._iterable_monadic_function)


################################################################################
# Decorator


def higher_order_iterable_monadic_function(higher_order_monadic_function):

    def higher_order_flippable_iterable_monadic_function(*args, **kwargs):
        monadic_function = higher_order_monadic_function(*args, *kwargs)
        return FlippableIterableMonadicFunction(monadic_function)

    return higher_order_flippable_iterable_monadic_function


################################################################################
#  Tee

_SINK_CHECKER__AND__TEE_HOIMF: list[_Callable, _Callable] = []


def register_tee(sink_checker: _Callable, tee_higher_order_iterable_monadic_function: _Callable):
    _SINK_CHECKER__AND__TEE_HOIMF.append([sink_checker, tee_higher_order_iterable_monadic_function])


@higher_order_iterable_monadic_function
def tee(sink: object, append: bool = False) -> _Callable:

    for key_f, tee_hoimf in _SINK_CHECKER__AND__TEE_HOIMF:
        if key_f(sink):
            tee_imf = tee_hoimf(sink, append)
            return tee_imf

    raise ValueError(f"sink=={sink} is not instance of either io, Sequence, or Set")


################################################################################
#  Tee for list
@higher_order_iterable_monadic_function
def tee_to_list(sink: object, append: bool = False) -> _Callable:

    def iterable_monadic_function(iterable: _Iterable) -> _Iterable[object]:

        def generator():
            if not append:
                sink.clear()
            for obj in iterable:
                sink.append(obj)
                yield obj

        return IterableMonad(generator())

    return iterable_monadic_function


register_tee(lambda sink: isinstance(sink, _Sequence), tee_to_list)

################################################################################
#  Tee for set


@higher_order_iterable_monadic_function
def tee_to_set(sink: object, append: bool = False) -> _Callable:

    def iterable_monadic_function(iterable: _Iterable) -> _Iterable[object]:

        def generator():
            if not append:
                sink.clear()
            for obj in iterable:
                sink.add(obj)
                yield obj

        return IterableMonad(generator())

    return iterable_monadic_function


register_tee(lambda sink: isinstance(sink, _Set), tee_to_set)
