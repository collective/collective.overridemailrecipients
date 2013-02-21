from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.sendmail.delivery import DirectMailDelivery, QueuedMailDelivery


def patchedSend(self, mfrom, mto, messageText, immediate=False):
    """ Send the message """

    patchedEmailAddress = getMailAddress()
    if patchedEmailAddress:
        mto = patchedEmailAddress

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
    email = registry['collective.testusermailpatch.configpanel.IMailPatchSettings.email']
    enabled = registry['collective.testusermailpatch.configpanel.IMailPatchSettings.enabled']
    print email, enabled
    if enabled:
        return email