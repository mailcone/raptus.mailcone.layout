import grok

from email.mime.text import MIMEText

from zope.component import getUtility
from zope import event, lifecycleevent

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import ISearchableContent, ISmtpServerUtil
from mfa_core_action.interfaces import IAction, IActionType, IActionContainer
from mfa_sendnotificationaction.interfaces import ISendNotificationAction

class SendNotificationAction(grok.Model, SearchableContentMixin):
    """ Provide a action for send notification mails """
    grok.implements(ISendNotificationAction, IAction, ISearchableContent)
    grok.context(IActionContainer)

    id = None
    content_type = 'SendNotificationAction'
    sortNr = None

    def __init__(self, id, to, subject, body, orgMail, match):
        """ Constructor """
        super(SendNotificationAction, self).__init__()
        self.id = id
        self.to = to
        self.subject = subject
        self.body = body
        self.match = match
        self.orgMail = orgMail

    def setSortNr(self, number):
        """XXX"""
        self.sortNr = number
        #reindexing
        event.notify(
            lifecycleevent.ObjectModifiedEvent(self, 
                                               lifecycleevent.Attributes(ISendNotificationAction, 'sortNr')
            )
        )

    grok.traversable('moveUp')
    def moveUp(self):
        return self.__parent__.moveActionUp(self)

    grok.traversable('moveDown')
    def moveDown(self):
        return self.__parent__.moveActionDown(self)

    def getActionTypeTitle(self):
        """ return title for registered filter type """
        return getUtility(IActionType, "SendNotificationActionType").title
    
    def apply(self):
        """ XXX """
        mail = MIMEText(self.body)
        mail['To'] = self.to
        mail['Subject'] = self.subject
        smtpUtil = getUtility(ISmtpServerUtil)
        smtpUtil.send(mail)