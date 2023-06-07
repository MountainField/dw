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

from dw.dsl import *

DATA: list[str] = ["a", "b"]


def DO_NOTHING_MF(iterable: _Iterable) -> IterableMonad:
    return IterableMonad(iterable)


with description("dw.dsl.IterableMonad"):

    with description("#bind"):

        @it("binds with new monad")
        def _(self):
            m = IterableMonad(DATA)
            m2 = m.bind(DO_NOTHING_MF)
            assert_that(m2.iterable, equal_to(DATA))

    with description("#__or__"):

        @it("binds with new monad")
        def _(self):
            m = IterableMonad(DATA)
            m2 = m | DO_NOTHING_MF
            assert_that(m2.iterable, equal_to(DATA))

    with description("#__iter__"):

        @it("behaves like Iterable")
        def _(self):
            assert_that(list(IterableMonad(["a", "b"])), equal_to(["a", "b"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
