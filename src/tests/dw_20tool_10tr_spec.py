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

from uspec import description, context, it, execute_command, shared_example_of
from hamcrest import assert_that, equal_to, instance_of, is_not

from dw.tool.tr import *
from dw.tool.tr import _tr2, _tr3, _tr4

from tests import dw_10dsl_spec

with description("dw.tool.tr.tr"):

    @it("replaces a single character ")
    def _(self):
        assert_that(list(IterableMonad(["abc", "xaz"]) | tr("a", "A")), equal_to(["Abc", "xAz"]))


with description("dw.tool.tr.tr2"):

    @it("replaces a single character ")
    def _(self):
        assert_that(list(IterableMonad(["abc", "xaz"]) | _tr2("a", "A")), equal_to(["Abc", "xAz"]))


with description("dw.tool.tr.tr3"):

    @it("replaces a single character ")
    def _(self):
        assert_that(list(IterableMonad(["abc", "xaz"]) | _tr3("a", "A")), equal_to(["Abc", "xAz"]))


with description(_tr4("a", "A")):
    it.behaves_like("iterable_monadic_function")

with description("dw.tool.tr.tr4"):

    @it("replaces a single character ")
    def _(self):
        assert_that(list(IterableMonad(["abc", "xaz"]) | _tr4("a", "A")), equal_to(["Abc", "xAz"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
