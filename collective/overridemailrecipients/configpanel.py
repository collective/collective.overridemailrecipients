from zope.interface import Interface
from zope import schema
from Products.CMFCore.interfaces import ISiteRoot

from plone.z3cform import layout
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

class IMailPatchSettings(Interface):
    """ Define settings data structure """

    email=schema.TextLine(
        title=u"Email address",
        description=u"This email address is used as recipient for all mails sent thru Plone",
        required=False,
    )
    enabled=schema.Bool(
        title=u"Enabled",
        description=u"When enabled all mail is sent to above mail address.",
    )

class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IMailPatchSettings
    description = u"Sent all mails sent in Plone to one email address"


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
SettingsView.label = u"collective.overridemailrecipient"