import grok

from zope.component import getUtilitiesFor, getUtility
from fanstatic import Library, Resource
from js.jquery import jquery

from mfa_core_action.interfaces import (
    IActionManager, 
    IActionType, 
    IActionMatchTypeManager, 
    IActionMatchType
)
from mailfilter.interfaces import IControlPanelJSExtention

class ActionManager(grok.GlobalUtility):
    """ manage registered actions """
    grok.implements(IActionManager)
    
    def listActionTypes(self, context):
        """
            return a dict of all registered filterType utils - dict provides keys 
            (title and url), the context must be a view object
        """
        actionUtils = getUtilitiesFor(IActionType)
        return [{'title':util[1].title,'url':context.url(util[1].addFormName)} for util in actionUtils]

    def listActionSettings(self):
        """ XXX """
        actionUtils = getUtilitiesFor(IActionType)
        return [{'title':util[1].title,'settingObj':util[1].getSettingObject()} for util in actionUtils]

class ActionJSExtender(grok.GlobalUtility):    
    """ XXX """
    grok.implements(IControlPanelJSExtention)
    grok.name('ActionJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_core_action', 'static')
        extension = Resource(library, 'action_jsextender.js', depends=[jquery])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions

#XXX - make base object
class ActionMatchTypeManager(grok.GlobalUtility):
    """ XXX """
    grok.implements(IActionMatchTypeManager)
    
    def getUtilKeys(self):
        """ XXX """
        sources = getUtilitiesFor(IActionMatchType)
        return [source[0] for source in sources]

    def getUtil(self,id):
        """ XXX """
        return getUtility(IActionMatchType, id)