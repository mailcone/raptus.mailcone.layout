import grok
from fanstatic import Library, Resource

from mailfilter.resource import rulesetJsExtender
from mailfilter.interfaces import IControlPanelJSExtention

from mfa_core_filter.interfaces import IFilterType

class SimpleMatchFilterType(grok.GlobalUtility):
    """ Utility provide filter type simple match for filter manager """
    grok.implements(IFilterType)
    grok.name('SimpleMatchFilterType')

    title = 'simple match'
    addFormName = 'addSimpleMatchFilter'
    
    def getSettingObject(self):
        """ XXX """
        pass
    
class SimpleMatchFilterJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('SimpleMatchFilterJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_simplematchfilter', 'static')
        extension = Resource(library, 'simplematchfilter_jsextender.js', depends=[rulesetJsExtender])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions