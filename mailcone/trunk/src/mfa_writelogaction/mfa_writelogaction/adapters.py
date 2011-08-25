import grok

from mailfilter.interfaces import ICopy
from mfa_writelogaction.interfaces import IWriteLogAction
from mfa_writelogaction.contents import WriteLogAction

class CopyWriteLogAction(grok.Adapter):
    """ Adapter provide ICopy for write log objects """
    grok.implements(ICopy)
    grok.context(IWriteLogAction)
    
    def copy(self, context):
        """ duplicate instance and save new instance in the given context """
        #XXX should check the given context provide ActionContainer
        newRule = context
        obj = self.context
        nextId = newRule.getNextId()
        newAction = WriteLogAction(nextId, obj.logfile, obj.loglevel, obj.logmessage, obj.match)
        newRule.addAction(newAction)