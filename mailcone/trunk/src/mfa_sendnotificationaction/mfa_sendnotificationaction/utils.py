import grok
from fanstatic import Library, Resource

from mailfilter.resource import rulesetJsExtender
from mailfilter.interfaces import IControlPanelJSExtention
from mfa_core_action.interfaces import IActionType

class SendNotificationActionType(grok.GlobalUtility):
    """ Utility provide action type send notification for filter manager """
    grok.implements(IActionType)
    grok.name('SendNotificationActionType')
    
    title = 'send notification'
    addFormName = 'addSendNotificationAction'
    
    def getSettingObject(self):
        """ XXX """
        pass
    
class SendNotificationActionJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('SendNotificationActionJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_sendnotificationaction', 'static')
        extension = Resource(library, 'sendnotificationaction_jsextender.js', depends=[rulesetJsExtender])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions