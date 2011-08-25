import grok

from mfa_writelogaction.interfaces import ILoglevelUtil

class LoglevelUtil(object):
    """ XXX """
    grok.implements(ILoglevelUtil)
    
    name = None

class InfoLoglevelUtil(LoglevelUtil, grok.GlobalUtility):
    """ XXX """
    grok.name('info')
    
    name = 'Info'

class WarningLoglevelUtil(LoglevelUtil, grok.GlobalUtility):
    """ XXX """
    grok.name('warning')
    
    name = 'Warning'
    
class ErrorLoglevelUtil(LoglevelUtil, grok.GlobalUtility):
    """ XXX """
    grok.name('error')
    
    name = 'Error'