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


####
def do_nothing_monadic_func1(iterable: _Iterable) -> IterableMonad:
    return IterableMonad(iterable)


####
class DoNothingMFClassBased(AbstractIterableMonadicFunction):

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable)


do_nothing_monadic_func_class_based = DoNothingMFClassBased()


####
class DoNothingMFFlippableClassBased(FlippableIterableMonadicFunction):

    def __init__(self):
        super().__init__(monadic_function=do_nothing_monadic_func1)


do_nothing_monadic_func_flippable_class_based = DoNothingMFFlippableClassBased()

with description("dw.dsl.IterableMonad"):

    ################################
    # Specs for v0.0.0
    with description("#__iter__"):

        @it("behaves like Iterable")
        def _(self):
            assert_that(list(IterableMonad(["a", "b"])), equal_to(["a", "b"]))

    ################################
    # Specs for v0.1.0
    for k, do_nothing_mf in {"function based": do_nothing_monadic_func1, \
                             "class based": do_nothing_monadic_func_class_based, \
                             "flippable class based": do_nothing_monadic_func_flippable_class_based}.items():

        with context(f"{k} monadic function"):
            with description("#bind"):

                @it("binds with new monad")
                def _(self):
                    m = IterableMonad(DATA)
                    m2 = m.bind(do_nothing_mf)
                    assert_that(m2.iterable, equal_to(DATA))

            with description("#__or__"):

                @it("binds with new monad")
                def _(self):
                    m = IterableMonad(DATA)
                    m2 = m | do_nothing_mf
                    assert_that(m2.iterable, equal_to(DATA))

    ################################
    # Specs for v0.2.0
    with description("#redirect_to"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that(IterableMonad(["a", "b"]).redirect_to([]), equal_to(["a", "b"]))

    with description("#__gt__"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that(IterableMonad(["a", "b"]) > [], equal_to(["a", "b"]))

    with description("#appending_redirect_to"):

        @it("puts recoreds into sink with append mode")
        def _(self):
            assert_that(IterableMonad(["a", "b"]).appending_redirect_to(["x"]), equal_to(["x", "a", "b"]))

    with description("#__rshift__"):

        @it("puts recoreds into sink with append mode")
        def _(self):
            assert_that(IterableMonad(["a", "b"]) >> ["x"], equal_to(["x", "a", "b"]))


with description("dw.dsl.FlippableIterableMonadicFunction"):

    ################################
    # Specs for v0.3.0
    with description("#__call__"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that((IterableMonad(["a", "b"]) | do_nothing_monadic_func_flippable_class_based) > [], equal_to(["a", "b"]))

    with description("#__ror__"):

        @it("puts recoreds into sink")
        def _(self):
            assert_that((["a", "b"] | do_nothing_monadic_func_flippable_class_based) > [], equal_to(["a", "b"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
