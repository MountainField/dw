# -*- coding: utf-8 -*-

# =================================================================
# dw
#
# Copyright (c) 2023 Takahide Nogayama
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# =================================================================

from uspec import description, context, it, execute_command
from hamcrest import assert_that, equal_to, instance_of, is_not

with description("dw"):

    @it("can be imported")
    def _(self):
        import dw
        assert_that(dw, is_not(None))


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
