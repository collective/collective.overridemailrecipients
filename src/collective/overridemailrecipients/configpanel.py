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
        description=u"Mails are always sent to 'plone@localhost', enter an email address to change de default address.",
        required=False,
        default=u'plone@localhost'
    )
    enabled=schema.Bool(
        title=u"Enabled",
        description=u"Disable mail forwarding.",
        default=True
    )

class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IMailPatchSettings
    description = u"Sent all mails to one email address"


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
SettingsView.label = u"collective.overridemailrecipient"