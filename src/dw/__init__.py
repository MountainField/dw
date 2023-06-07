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

__version__ = "0.3.0"

import logging as _logging
import os as _os
import sys as _sys

# Logger
_LOGGER: _logging.Logger = _logging.getLogger(__name__)
_LOG_FORMAT: str = '%(asctime)s |  %(levelname)-7s | %(message)s (%(filename)s L%(lineno)s %(name)s)'

from . import dsl


################################################################################
def main_cli(*args: list[str]) -> int:
    _logging.basicConfig(stream=_sys.stderr, format=_LOG_FORMAT, level=_logging.INFO)
    print("hello")
    return 0


if __name__ == "__main__":
    _sys.exit(main_cli())
