import grok

from zope import schema, interface
from zope.interface import Interface
from zope.schema.interfaces import IIterableSource
from zope.schema.vocabulary import SimpleTerm
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.browser.interfaces import ITerms
from zope.component import getUtility

from mfa_core_action.interfaces import ActionMatchTypes

class ILogfile(Interface):
    """ XXX """
    
    id = interface.Attribute('id')
    name = schema.TextLine(title=u'Title', required=True)
    logfile = schema.TextLine(title=u'logfile', required=True)
    filepath =  schema.TextLine(title=u'filepath', required=True)

class ILogfileManager(Interface):
    """ XXX """
    
    def getLogfileIds():
        """ XXX """
    
    def getLogfileById(id):
        """ XXX """

class Logfiles(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(ILogfileManager)
        return manager.getLogfileIds()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class LogfileTerms(grok.MultiAdapter):
    grok.adapts(Logfiles, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(ILogfileManager)
        util = manager.getLogfileById(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token

class ILoglevelUtil(Interface):
    """ XXX """
    name = interface.Attribute('name')

class ILoglevelManager(Interface):
    """ XXX """
    
    def getLoglevelKeys():
        """ XXX """
    
    def getLoglevelUtil(id):
        """ XXX """

class Loglevels(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(ILoglevelManager)
        return manager.getLoglevelKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class LoglevelTerms(grok.MultiAdapter):
    grok.adapts(Loglevels, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(ILoglevelManager)
        util = manager.getLoglevelUtil(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token
    
class IWriteLogAction(Interface):
    """ Interface for write log action """
    match = schema.Choice(title=u'match',
                           source=ActionMatchTypes(),
                           required=True)
    logfile = schema.Choice(title=u'logfile',
                            source=Logfiles(),
                            required=True)
    loglevel = schema.Choice(title=u'loglevel',
                             source=Loglevels(),
                             required=True)
    logmessage = schema.TextLine(title=u'log message', required=True)

class IWriteLogActionSettingObject(Interface):
    """ Marker interface for write log action settings """
    
    id = interface.Attribute('id')
    title = interface.Attribute('title')
    form_name = interface.Attribute('form_name')

    def getLogfiles(self):
        """ return all logfiles registered in WriteLogActionSettingObject """
    
    def delLogfile(self, obj):
        """ delete give obj """