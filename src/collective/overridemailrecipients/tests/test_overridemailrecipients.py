""" Tests for collective.overridemailrecipients """

from Products.CMFCore.utils import getToolByName

import email
from mock import MagicMock
from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles, login, applyProfile
from plone.testing.z2 import Browser
from plone.app.controlpanel.mail import MailControlPanelAdapter
from plone.registry.interfaces import IRegistry
from plone.registry import field
from plone.registry.record import Record
import unittest2 as unittest
from zope.component import getUtility

from collective.overridemailrecipients.patches import get_mail_address
from collective.overridemailrecipients.testing import TEST_LAYER_INTEGRATION, TEST_LAYER_FUNCTIONAL

DEFAULT_MAIL = 'plone@localhost'
REG_MAIL = 'collective.overridemailrecipients.configpanel.IMailPatchSettings.email'
REG_ENABLED = 'collective.overridemailrecipients.configpanel.IMailPatchSettings.enabled'

MAIL_TEXT = u"""From: collective@example.org
To: somebody@example.org
Cc: carbon@example.org
Bcc: blind@example.org
Subject: Testing patched mailhost
Mime-Version: 1.0
Content-Type: text/html

<html>
<body>
This is a test.
</body>
</html>
"""


class TestOverrideMailRecipients(unittest.TestCase):

    layer = TEST_LAYER_FUNCTIONAL

    def setUp(self):
        """ Do the bootstrapping to get everything ready  """
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.mailhost = getToolByName(self.portal, 'MailHost')

        applyProfile(self.portal, 'collective.overridemailrecipients:default')
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Member'])

        mail_adapter = MailControlPanelAdapter(self.portal)
        mail_adapter.smtp_host = u'smtp.example.com'  # This is not used
        mail_adapter.email_from_address = u'noreply@example.com'
        mail_adapter.email_from_name = u'Gekke Henkie'

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.overridemailrecipients'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        u'package appears not to have been installed')

    def test_patch(self):
        """ Validate that MailHost sendmail is patched. Check is the to-header
        is changed and cc and bcc headers are stripped.
        """

        def _patched_makeMailer():
            """ Create a Dummy SMTPMailer and create a mock for send method """
            self.mock_mailer = MagicMock()
            self.mock_send = MagicMock()
            self.mock_mailer.send = self.mock_send
            return self.mock_mailer

        self.assertIn(
            "Monkey patched by** 'collective.overridemailrecipients.patches.patchedSend'",
            self.mailhost._send.__doc__,
            u'MailHost send is not patched'
        )

        self.mailhost._makeMailer = _patched_makeMailer  # Patch send mail
        self.mailhost.send(MAIL_TEXT, immediate=True)
        self.assertEqual(self.mock_mailer.send.called, True, 'Mock mail sent not called')

        # Get the arguments (and mail) which are given to mock send method
        kall = self.mock_mailer.send.mock_calls[0]
        name, arguments, kwargs = kall
        mail_txt = arguments[2]

        msg = email.message_from_string(mail_txt)
        self.assertEqual(
            msg['To'], 'plone@localhost',
            u'Dummy email address not found in To header not found'
        )
        self.assertFalse(msg['Cc'])
        self.assertFalse(msg['Bcc'])

    def test_get_mail_address(self):
        """ Test registry """

        self._reinstall()

        registry = getUtility(IRegistry)
        email = registry.get(REG_MAIL)
        enabled = registry.get(REG_ENABLED)

        self.assertEqual(email, u'plone@localhost')
        self.assertTrue(enabled, None)

        # When registry is 'empty', the default value is returned
        self.assertEqual(get_mail_address(), u'plone@localhost')

        # When registry value is stored, default value is returned
        # registry.records[REG_ENABLED] = Record(field.Bool(title=u'enabled'), True)
        registry[REG_ENABLED] = True
        self.assertEqual(get_mail_address(), u'plone@localhost')

        # Registry is enabled and has a stored mail address
        # registry.records[REG_MAIL] = Record(field.TextLine(title=u'mail'), u'henk@example.org')
        registry[REG_MAIL] = u'henk@example.org'
        self.assertEqual(get_mail_address(), u'henk@example.org')

        # Disable registry
        registry[REG_ENABLED] = False
        self.assertEqual(get_mail_address(), None)

    def test_controlpanel(self):

        self._reinstall()

        browser = Browser(self.app)

        # Login as site owner
        browser.open('{0}/login_form'.format(self.portal.absolute_url()))
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()
  
        browser.open('{0}/@@overridemailrecipients-settings'.format(self.portal.absolute_url()))
        self.assertEqual(
            browser.headers['status'], '200 Ok',
            u'Control panel is not available'
        )

        # Change mail address
        browser.getControl(label='Email address').value = u'henk@example.org'
        browser.getControl(label='Save').click()

        # Disable override
        browser.open('{0}/@@overridemailrecipients-settings'.format(self.portal.absolute_url()))
        browser.getControl(label='Enabled').selected=False
        browser.getControl(label='Save').click()
        self.assertEqual(get_mail_address(), None)

    def _reinstall(self):
        """ We must uninstall and install the package, it seems generic setup profile
        is not applied coorectly by plone.app.testing in this testing layer.
        """

        browser = Browser(self.app)

        # Login as site owner
        browser.open('{0}/login_form'.format(self.portal.absolute_url()))
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

        # We must uninstall and install the package, it seems generic setup profile
        # is not applied coorectly by plone.app.testing in this testing layer.
        browser.open('{0}/prefs_install_products_form'.format(self.portal.absolute_url()))

        form = browser.getForm(index=2)
        self.assertEqual(
            form.action, '{0}/portal_quickinstaller'.format(self.portal.absolute_url()),
            u'Uninstall form not found')
        form.getControl(name='products:list').value = (u"collective.overridemailrecipients",)
        form.getControl(label='Deactivate').click()

        form = browser.getForm(index=1)
        self.assertEqual(
            form.action, '{0}/portal_quickinstaller/installProducts'.format(self.portal.absolute_url()),
            u'Install form not found')
        form.getControl(name='products:list').value = (u"collective.overridemailrecipients",)
        form.getControl(label='Activate').click()


