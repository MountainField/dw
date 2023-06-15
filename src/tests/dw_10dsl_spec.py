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

import dw
from dw.dsl import *


####
def do_nothing_mf_v1(iterable: _Iterable) -> IterableMonad:
    return IterableMonad(iterable)


####
class DoNothingMFClassBased(AbstractIterableMonadicFunction):

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable)


do_nothing_mf_v2 = DoNothingMFClassBased()


####
class DoNothingMFFlippableClassBased(FlippableIterableMonadicFunction):

    def __init__(self):
        super().__init__(iterable_monadic_function=do_nothing_mf_v1)


do_nothing_mf_v3 = DoNothingMFFlippableClassBased()


@higher_order_iterable_monadic_function
def do_nothing_monadic_func_by_decorator_f():

    def f(iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable)

    return f


do_nothing_mf_v4 = do_nothing_monadic_func_by_decorator_f()

with description("dw.dsl.IterableMonad"):

    ################################
    # Specs for v0.0.0
    with description("#__iter__"):

        @it("behaves like Iterable")
        def _(self):
            assert_that(list(IterableMonad(["a", "b"])), equal_to(["a", "b"]))

    with description("#bind"):

        @it("returns a new monad")
        def _(self):
            m = IterableMonad(["a", "b"])
            m2 = m.bind(do_nothing_mf_v1)
            assert_that(m2, instance_of(IterableMonad))
            assert_that(m2.iterable, equal_to(["a", "b"]))

    with description("IterableMonad | mf"):

        @it("returns a new monad")
        def _(self):
            m = IterableMonad(["a", "b"])
            m2 = m | do_nothing_mf_v1
            assert_that(m2, instance_of(IterableMonad))
            assert_that(m2.iterable, equal_to(["a", "b"]))

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


################################
# Specs for v0.2.0
def monadic_function_v1_spec(name, mf, is_do_nothing=False):

    with context(f"monadic function: {name}"):

        with description("__call__(Iterable)"):

            @it("returns a new monad")
            def _(self):
                m2 = mf(["a", "b"])
                assert_that(m2, instance_of(IterableMonad))
                if is_do_nothing:
                    assert_that(m2.iterable, equal_to(["a", "b"]))


monadic_function_v1_spec("do_nothing_mf_v1", do_nothing_mf_v1, is_do_nothing=True)
monadic_function_v1_spec("do_nothing_mf_v2", do_nothing_mf_v2, is_do_nothing=True)


################################
# Specs for v0.3.0
def monadic_function_v3_spec(name, mf, is_do_nothing=False):

    with context(f"monadic function: {name}"):

        with description("__ror__(Iterable)"):

            @it("returns a new monad")
            def _(self):
                m2 = ["a", "b"] | mf
                assert_that(m2, instance_of(IterableMonad))
                if is_do_nothing:
                    assert_that(m2.iterable, equal_to(["a", "b"]))


monadic_function_v1_spec("do_nothing_mf_v3", do_nothing_mf_v3, is_do_nothing=True)
monadic_function_v3_spec("do_nothing_mf_v3", do_nothing_mf_v3, is_do_nothing=True)


def monadic_function_all_spec(name, mf, is_do_nothing=False):
    print("name: ", name)
    monadic_function_v1_spec(name, mf, is_do_nothing)
    monadic_function_v3_spec(name, mf, is_do_nothing)


monadic_function_all_spec("do_nothing_mf_v4", do_nothing_mf_v4, is_do_nothing=True)

monadic_function_all_spec("tee_to_set", dw.dsl.tee_to_set(set()))
monadic_function_all_spec("tee", dw.dsl.tee([]))

################################
# Specs for v0.5.0
monadic_function_all_spec("dw.dsl.tee_to_list", dw.dsl.tee_to_list([]))

with description("dw.dsl.tee_to_list"):

    @it("puts recoreds into list sink")
    def _(self):
        l = []
        consume(IterableMonad(["a", "b"]) | tee_to_list(l))
        assert_that(l, equal_to(["a", "b"]))

    @it("puts recoreds into list sink")
    def _(self):
        l = []
        consume(["a", "b"] | tee_to_list(l))
        assert_that(l, equal_to(["a", "b"]))

    @it("puts recoreds into list sink")
    def _(self):
        l = []
        l2 = IterableMonad(["a", "b"]) > l
        assert_that(l, equal_to(["a", "b"]))
        assert_that(l2, equal_to(["a", "b"]))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
