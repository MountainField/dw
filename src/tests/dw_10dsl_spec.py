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

    ################################
    # Specs from v0.0.0
    with description("#__iter__"):

        @it("behaves like Iterable")
        def _(self):
            assert_that(list(IterableMonad(["a", "b"])), equal_to(["a", "b"]))

    ################################
    # Specs from v0.1.0
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

    ################################
    # Specs from v0.2.0
    with description("#redirect_to"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that(IterableMonad(["a", "b"]).redirect_to([]), equal_to(["a", "b"]))

    with description("#__gt__"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that(IterableMonad(["a", "b"]) > [], equal_to(["a", "b"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
