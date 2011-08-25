# grok stuff
import grok

from mailfilter.interfaces import ICopy, IRule
from mailfilter.contents import Rule

class CopyRuleAdapter(grok.Adapter):
    """ Adapter provide ICopy for rule objects """
    grok.implements(ICopy)
    grok.context(IRule)
    
    def copy(self, context):
        """ duplicate instance and save new instance in the given context """
        newContainer = context
        obj = self.context
        #XXX - what happen if id already exists?
        newRule = Rule(obj.name, obj.description, obj.severity, obj.matching)
        newContainer.addRule(newRule)
        #XXX - copy of childrens - not implemented yet
        for child in obj.values():
            ICopy(child).copy(newRule)