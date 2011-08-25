"""
    Utils for rule expected mail period unit
"""
import grok

from mailfilter.interfaces import IPeriodUnit

class PeriodUnit(object):
    """ XXX """
    grok.implements(IPeriodUnit)
    name = None

class PeriodUnitHour(PeriodUnit, grok.GlobalUtility):
    """ XXX """
    grok.name('hour')    
    name = 'Hour(s)'

class PeriodUnitDay(PeriodUnit, grok.GlobalUtility):
    """ XXX """
    grok.name('day')    
    name = 'Day(s)'

class PeriodUnitMonth(PeriodUnit, grok.GlobalUtility):
    """ XXX """
    grok.name('month')
    name = 'Month(s)'