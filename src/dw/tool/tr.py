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
from __future__ import annotations

from collections.abc import Callable as _Callable
from collections.abc import Iterable as _Iterable

import logging as _logging
import os as _os
import sys as _sys

# Logger
_LOGGER: _logging.Logger = _logging.getLogger(__name__)

from dw.dsl import *
"""
- https://www.geeksforgeeks.org/tr-command-in-unix-linux-with-examples/
- https://linuxcommand.org/lc3_man_pages/tr1.html
"""


################################
# based on v0.1.0
def tr1(set1: str, set2: str) -> _Callable:

    def monadic_func(iterable: _Iterable[str]) -> _Iterable[str]:
        row_in: str
        row_out: str
        for row_in in iterable:
            if set1 in row_in:
                row_out = row_in.replace(set1, set2)
            else:
                row_out = row_in
            yield row_out

    return monadic_func


tr = tr1


################################
# based on v0.2.0
class _tr2(AbstractIterableMonadicFunction):

    def __init__(self, set1: str, set2: str):
        self.f = tr1(set1, set2)

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return self.f(iterable)


################################
# based on v0.3.0
class _tr3(FlippableIterableMonadicFunction):

    def __init__(self, set1: str, set2: str):
        super().__init__(monadic_function=tr1(set1, set2))


################################
# based on v0.4.0
@pipeable
def _tr4(set1: str, set2: str) -> _Callable:

    def mf(iterable: _Iterable[str]) -> _Iterable[str]:
        row_in: str
        row_out: str
        for row_in in iterable:
            if set1 in row_in:
                row_out = row_in.replace(set1, set2)
            else:
                row_out = row_in
            yield row_out

    return mf
