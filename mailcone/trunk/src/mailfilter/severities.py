"""
    Utils for severities
"""
import grok

from mailfilter.interfaces import ISeverity

class Severity(object):
    """ Base object for severities - used in rule objects """
    grok.implements(ISeverity)
    name = None

class High(Severity, grok.GlobalUtility):
    """ XXX """
    grok.name('high')    
    name = 'High'

class Middle(Severity, grok.GlobalUtility):
    """ XXX """
    grok.name('middle')    
    name = 'Middle'

class Low(Severity, grok.GlobalUtility):
    """ XXX """
    grok.name('low')
    name = 'Low'