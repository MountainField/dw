# -*- coding: utf-8 -*-

# =================================================================
# dw
#
# Copyright (c) 2023 Takahide Nogayama
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# =================================================================

__version__: str = "0.6.1"

import logging as _logging
import sys as _sys

# Logger
_LOGGER: _logging.Logger = _logging.getLogger(__name__)
_LOG_FORMAT: str = '%(asctime)s |  %(levelname)-7s | %(message)s (%(filename)s L%(lineno)s %(name)s)'

DEFAULT_ENCODING: str = "utf-8"

if __name__ == "__main__":
    _logging.basicConfig(stream=_sys.stderr, format=_LOG_FORMAT, level=_logging.WARNING)
