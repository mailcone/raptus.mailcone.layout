import grok

from mfa_core_action.interfaces import IActionMatchType

class ActionMatchType(object):
    """ XXX """
    grok.implements(IActionMatchType)
    name = None
    
    def apply(self, action, resultMails):
        """ XXX """
        pass

class ActionMatchTypeMatch(ActionMatchType, grok.GlobalUtility):
    """ XXX """
    grok.name('match')    
    name = 'if match'

    def apply(self, action, resultMails):
        """ XXX """
        if resultMails:
            action.apply()

class ActionMatchTypeNotMatch(ActionMatchType, grok.GlobalUtility):
    """ XXX """
    grok.name('not match')
    name = 'if does not match'
    
    def apply(self, action, resultMails):
        """ XXX """
        if not resultMails:
            action.apply()