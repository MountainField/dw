# -*- coding: utf-8 -*-

# =================================================================
# Licensed Materials - Property of IBM
#
# (c) Copyright IBM Corp. 2021, 2021 All Rights Reserved
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
# =================================================================

from collections.abc import Iterable as _Iterable

from uspec import description, context, it, execute_command
from hamcrest import assert_that, equal_to, instance_of, is_not

from dw.tool.tr import *

with description("dw.tool.tr.tr"):

    @it("replaces a single character ")
    def _(self):
        assert_that(list(IterableMonad(["abc", "xaz"]) | tr("a", "A")), equal_to(["Abc", "xAz"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
