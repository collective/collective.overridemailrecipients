""" General tests """

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login

from collective.testusermailpatch.testing import OPSB_CONTENT_INTEGRATION

class TestGeneral(unittest.TestCase):

    layer = OPSB_CONTENT_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.testusermailpatch'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        u'package appears not to have been installed')