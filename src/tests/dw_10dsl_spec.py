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

import dw
from dw.dsl import *


####
def do_nothing_mf_v1(iterable: _Iterable) -> IterableMonad:
    return IterableMonad(iterable)


####
class DoNothingMFClassBased(AbstractIterableMonadicFunction):

    def __init__(self):
        self.__name__ = "do_nothing_mf_v2"

    def __call__(self, iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable)


do_nothing_mf_v2 = DoNothingMFClassBased()


####
class DoNothingMFFlippableClassBased(FlippableIterableMonadicFunction):

    def __init__(self):
        super().__init__(iterable_monadic_function=do_nothing_mf_v1)


do_nothing_mf_v3 = DoNothingMFFlippableClassBased()


@higher_order_iterable_monadic_function
def do_nothing_hoimf_v4():

    def f(iterable: _Iterable) -> IterableMonad:
        return IterableMonad(iterable)

    return f


do_nothing_mf_v4 = do_nothing_hoimf_v4()


@higher_order_generator_function
def do_nothing_hoimf_v7():

    def g(iterable: _Iterable) -> IterableMonad:
        return iterable

    return g


do_nothing_mf_v7 = do_nothing_hoimf_v7()

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
@shared_example_of("v1")
def _(mf, is_do_nothing=False, context_stack=[]):

    with context(f"monadic function: {mf.__name__}"):

        with description("__call__(Iterable)"):

            @it("returns a new monad")
            def _(self):
                m2 = mf(["a", "b"])
                assert_that(m2, instance_of(IterableMonad))
                if is_do_nothing:
                    assert_that(m2.iterable, equal_to(["a", "b"]))


with description(do_nothing_mf_v1):
    it.behaves_like("v1", is_do_nothing=True)

with description(do_nothing_mf_v2):
    it.behaves_like("v1", is_do_nothing=True)


################################
# Specs for v0.3.0
@shared_example_of("v3")
def _(mf, is_do_nothing=False, context_stack=[]):

    with context(f"monadic function: {mf.__name__}"):

        with description("__ror__(Iterable)"):

            @it("returns a new monad")
            def _(self):
                m2 = ["a", "b"] | mf
                assert_that(m2, instance_of(IterableMonad))
                if is_do_nothing:
                    assert_that(m2.iterable, equal_to(["a", "b"]))


with description(do_nothing_mf_v3):
    it.behaves_like("v1", is_do_nothing=True)
    it.behaves_like("v3", is_do_nothing=True)


@shared_example_of("iterable_monadic_function")
def _(mf, is_do_nothing=False, context_stack=[]):

    with description(mf):

        it.behaves_like("v1", is_do_nothing=is_do_nothing)
        it.behaves_like("v3", is_do_nothing=is_do_nothing)


with description(do_nothing_mf_v4):
    it.behaves_like("iterable_monadic_function", is_do_nothing=True)

with description(do_nothing_mf_v7):
    it.behaves_like("iterable_monadic_function", is_do_nothing=True)

with description(dw.dsl.tee_to_set(set())):
    it.behaves_like("iterable_monadic_function")

################################
# Specs for v0.5.0

with description(dw.dsl.tee_to_list([])):
    it.behaves_like("iterable_monadic_function")

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
