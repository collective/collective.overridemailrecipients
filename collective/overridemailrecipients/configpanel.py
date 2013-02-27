from zope.interface import Interface
from zope import schema
from Products.CMFCore.interfaces import ISiteRoot

from plone.z3cform import layout
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

class IMailPatchSettings(Interface):
    """ Define settings data structure """

    email = schema.TextLine(title = u"Test user enmail address",
                            description = u"Email address to send all mails in the test environment",
                            required = False)
    enabled_plone = schema.Bool(title = u"Enabled",
                          description = u"If the patch is enabled all mails will be sent to provided email address")

    enabled_env = schema.Bool(title = u"Enabled",
                                description = u"If the patch is enabled all mails will be sent to provided email address")


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IMailPatchSettings
    label = u"Override email recipient settings"
    description = u"Override the recipients in all emails sent"


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
SettingsView.label = u"Mail patch settings"