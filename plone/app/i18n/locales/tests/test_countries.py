# -*- coding: UTF-8 -*-
"""
    Country tests.
"""

import paitestcase
import unittest

from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite

from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.app.i18n.locales.countries'),
        Suite('countries.txt',
            optionflags=OPTIONFLAGS,
            package='plone.app.i18n.locales.tests',
            test_class=paitestcase.FunctionalTestCase
            )
        ))
