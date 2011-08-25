import grok

from zope.component import getUtilitiesFor, getUtility
from fanstatic import Library, Resource
from js.jquery import jquery

from mfa_core_filter.interfaces import (
    IFilterManager, 
    IFilterType,
    IMailSource,
    IMailSourceManager, 
    ISimpleFilterOperator,
    ISimpleFilterOperatorManager
)
from mailfilter.interfaces import IControlPanelJSExtention

# XXX - should be done in mailfilter
class FilterJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('FilterJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_core_filter', 'static')
        extension = Resource(library, 'filter_jsextender.js', depends=[jquery])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions

class FilterManager(grok.GlobalUtility):
    """ manage registered filters """
    grok.implements(IFilterManager)
    
    def listFilterTypes(self, context):
        """
            return a dict of all registered filterType utils - dict provides keys 
            (title and url), the context must be a view object
        """
        filterUtils = getUtilitiesFor(IFilterType)
        return [{'title':util[1].title,'url':context.url(util[1].addFormName)} for util in filterUtils]

    def listFilterSettings(self):
        """ XXX """
        filterUtils = getUtilitiesFor(IFilterType)
        return [{'title':util[1].title,'settingObj':util[1].getSettingObject()} for util in filterUtils]

class SimpleFilterOperatorManager(grok.GlobalUtility):
    """ XXX """
    grok.implements(ISimpleFilterOperatorManager)
    
    def getSourceKeys(self):
        """ XXX """
        sources = getUtilitiesFor(ISimpleFilterOperator)
        return [source[0] for source in sources]

    def getSource(self,id):
        """ XXX """
        return getUtility(ISimpleFilterOperator, id)

    def apply(self, operator, filterCondition, source):
        """ XXX """
        operatorUtil = getUtility(ISimpleFilterOperator, operator)
        return operatorUtil.apply(filterCondition, source)

#XXX move to mail package
class MailSourceManager(grok.GlobalUtility):
    """ XXX """
    grok.implements(IMailSourceManager)
    
    def getSourceKeys(self):
        """ XXX """
        sources = getUtilitiesFor(IMailSource)
        return [source[0] for source in sources]

    def getSourceUtil(self,id):
        """ XXX """
        return getUtility(IMailSource, id)
    
    def getSource(self, id, obj):
        """ XXX """
        sourceUtil = getUtility(IMailSource, id)
        return sourceUtil.getSource(obj)