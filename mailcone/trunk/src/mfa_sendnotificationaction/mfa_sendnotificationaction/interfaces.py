from zope import schema
from zope.interface import Interface

from mfa_core_action.interfaces import ActionMatchTypes

class ISendNotificationAction(Interface):
    """ Interface for send notification action """
    match = schema.Choice(title=u'match',
                          source=ActionMatchTypes(),
                          required=True)
    to = schema.TextLine(title=u'to',required=True)
    subject = schema.TextLine(title=u'subject', required=True)
    body = schema.Text(title=u'Text',required=True)
    orgMail = schema.Bool(title=u'attach org. mail', required=False)