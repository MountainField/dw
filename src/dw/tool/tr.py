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
def tr(set1: str, set2: str) -> _Callable:

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
