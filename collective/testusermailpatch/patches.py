from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.sendmail.delivery import DirectMailDelivery, QueuedMailDelivery
from copy import deepcopy
from email.Message import Message
from email import message_from_string
from interfaces import IThemeSpecific
from plone.browserlayer.utils import registered_layers

def patchedSend(self, mfrom, mto, messageText, immediate=False):
    """ Send the message """
    if IThemeSpecific in registered_layers():
        patchedEmailAddress = getMailAddress()
        if patchedEmailAddress:
            mto = patchedEmailAddress
            if isinstance(messageText, Message):
                # We already have a message, make a copy to operate on
                mo = deepcopy(messageText)
            else:
                # Otherwise parse the input message
                mo = message_from_string(messageText)
            if mo.get('Bcc'):
                del mo['Bcc']
            if mo.get('Cc'):
                del mo['Cc']
            if mo.get('To'):
                del mo['To']
            mo['To'] = mto
            messageText = mo.as_string()


    if immediate:
        self._makeMailer().send(mfrom, mto, messageText)
    else:
        if self.smtp_queue:
            # Start queue processor thread, if necessary
            self._startQueueProcessorThread()
            delivery = QueuedMailDelivery(self.smtp_queue_directory)
        else:
            delivery = DirectMailDelivery(self._makeMailer())

        delivery.send(mfrom, mto, messageText)

def getMailAddress():
    registry = getUtility(IRegistry)
    email = registry.get('collective.testusermailpatch.configpanel.IMailPatchSettings.email')
    enabled = registry.get('collective.testusermailpatch.configpanel.IMailPatchSettings.enabled')
    print email, enabled
    if enabled and email:
        return email
