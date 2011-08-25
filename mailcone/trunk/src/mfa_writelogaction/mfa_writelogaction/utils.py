import grok
from fanstatic import Library, Resource
from zope.component import getUtilitiesFor, getUtility

from mailfilter.resource import rulesetJsExtender
from mailfilter.interfaces import IControlPanelJSExtention
from mfa_core_action.interfaces import IActionType

from mfa_writelogaction.interfaces import ILogfileManager, ILogfile, ILoglevelManager, ILoglevelUtil, IWriteLogActionSettingObject
from mfa_writelogaction.settings import WirteLogActionSettingObject

# catalog stuff
from hurry.query.interfaces import IQuery
from hurry.query import set, Eq, And

class WrtieLogActionType(grok.GlobalUtility):
    """ Utility provide action type write log for filter manager """
    grok.implements(IActionType)
    grok.name('WriteLogActionType')
    
    title = 'write log'
    addFormName = 'addWriteLogAction'
    
    def getSettingObject(self):
        """ XXX """
        query = getUtility(IQuery)
        result = query.searchResults(set.AnyOf(('catalog', 'implements'), [IWriteLogActionSettingObject.__identifier__,]))
        if result.__len__() == 0:
            container = grok.getApplication()
            settingObj = WirteLogActionSettingObject()
            container[settingObj.id] = settingObj
            return settingObj
        return [obj for obj in result][0]
    
class WrtieLogActionJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('WrtieLogActionJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_writelogaction', 'static')
        extension = Resource(library, 'writelogaction_jsextender.js', depends=[rulesetJsExtender])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions
    
class LogfileManager(grok.GlobalUtility):
    """ XXX """
    grok.implements(ILogfileManager)
    
    def getLogfileIds(self):
        """ XXX """
        query = getUtility(IQuery)
        logfiles = query.searchResults(set.AnyOf(('catalog', 'implements'), [ILogfile.__identifier__,]))
        return [logfile.id for logfile in logfiles]

    def getLogfileById(self,id):
        """ XXX """
        query = getUtility(IQuery)
        logfiles = query.searchResults(set.AnyOf(('catalog', 'implements'), [ILogfile.__identifier__,]) &
                                       Eq(('catalog', 'id'), id))
        return [file for file in logfiles][0]
    
class LoglevelManager(grok.GlobalUtility):
    """ XXX """
    grok.implements(ILoglevelManager)
    
    def getLoglevelKeys(self):
        """ XXX """
        sources = getUtilitiesFor(ILoglevelUtil)
        return [source[0] for source in sources]
    
    def getLoglevelUtil(self, id):
        """ XXX """
        return getUtility(ILoglevelUtil, id)