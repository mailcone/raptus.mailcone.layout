import grok
from fanstatic import Library, Resource

from mailfilter.resource import rulesetJsExtender
from mailfilter.interfaces import IControlPanelJSExtention
from mfa_core_filter.interfaces import IFilterType

class PythonCodeFilterType(grok.GlobalUtility):
    """ Utility provide filter type python code for filter manager """
    grok.implements(IFilterType)
    grok.name('PythonCodeFilterType')
    
    title = 'python code'
    addFormName = 'addPythonFilter'
    
    def getSettingObject(self):
        """ XXX """
        pass
    
class PythonCodeFilterJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('PythonCodeFilterJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_pythoncodefilter', 'static')
        extension = Resource(library, 'pythoncodefilter_jsextender.js', depends=[rulesetJsExtender])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions