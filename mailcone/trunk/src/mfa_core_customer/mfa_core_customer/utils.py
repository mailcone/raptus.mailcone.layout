# grok stuff
import grok

from zope.component import getUtilitiesFor
from fanstatic import Library, Resource
from js.jquery import jquery

from mailfilter.interfaces import IControlPanelJSExtention

class CustomerConfigletJSExtender(grok.GlobalUtility):    
    """ XXX - test"""
    grok.implements(IControlPanelJSExtention)
    grok.name('CustomerConfigletJSExtender')
    jsExtensions = []
    
    def __init__(self):
        library = Library('mfa_core_customer', 'static')
        extension = Resource(library, 'customer_jsextender.js', depends=[jquery])
        self.jsExtensions.append(extension)

    def listExtensions(self):
        return self.jsExtensions