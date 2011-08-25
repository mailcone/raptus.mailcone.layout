import grok

from mailfilter.interfaces import ICopy
from mfa_pythoncodefilter.interfaces import IPythonCodeFilter 
from mfa_pythoncodefilter.contents import PythonCodeFilter

class CopyPythonCodeFilter(grok.Adapter):
    """ Adapter provide ICopy for python code filter objects """
    grok.implements(ICopy)
    grok.context(IPythonCodeFilter)
    
    def copy(self, context):
        """ duplicate instance and save new instance in the given context """
        newRule = context
        obj = self.context
        nextId = newRule.getNextId()
        newFilter = PythonCodeFilter(nextId, obj.code)
        newRule.addFilter(newFilter)