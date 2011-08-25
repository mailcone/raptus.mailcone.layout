import grok

from mailfilter.interfaces import ICopy
from mfa_complexmatchfilter.interfaces import IComplexMatchFilter 
from mfa_complexmatchfilter.contents import ComplexMatchFilter

class CopyComplexMatchFilter(grok.Adapter):
    """ Adapter provide ICopy for complex match filter objects """
    grok.implements(ICopy)
    grok.context(IComplexMatchFilter)
    
    def copy(self, context):
        """ duplicate instance and save new instance in the given context """
        newRule = context
        obj = self.context
        nextId = newRule.getNextId()
        newFilter = ComplexMatchFilter(nextId, obj.source, obj.condition)
        newRule.addFilter(newFilter)