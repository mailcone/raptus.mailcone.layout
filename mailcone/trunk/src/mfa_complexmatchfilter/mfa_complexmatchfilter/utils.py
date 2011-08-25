import grok
from fanstatic import Library, Resource

from mailfilter.resource import rulesetJsExtender
from mailfilter.interfaces import IControlPanelJSExtention
from mfa_core_filter.interfaces import IFilterType

class ComplexMatchFilterType(grok.GlobalUtility):
    """ Utility provide filter type complex match for filter manager """
    grok.implements(IFilterType)
    grok.name('ComplexMatchFilterType')
    
    title = 'complex match'
    addFormName = 'addComplexMatchFilter'

    def getSettingObject(self):
        """ XXX """
        pass
    
class ComplexMatchFilterJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('ComplexMatchFilterJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_complexmatchfilter', 'static')
        extension = Resource(library, 'complexmatchfilter_jsextender.js', depends=[rulesetJsExtender])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions