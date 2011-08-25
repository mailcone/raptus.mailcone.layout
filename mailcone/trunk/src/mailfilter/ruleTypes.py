"""
    Utils for rule types
"""
import grok
from datetime import datetime
from megrok import rdb

from zope.component import getUtility
from mfa_core_action.interfaces import IActionMatchType
from mailfilter.interfaces import IRuleType

class RuleType(object):
    """ Base object for rule types """
    grok.implements(IRuleType)
    name = None
    mails = None
    rule = None

    def apply(self, mails, rule):
        """ XXX """
        self.mails = mails
        self.rule = rule
    
    def markMatchedMails(self, matchedMails):
        """ XXX """
        for mail in matchedMails:
            session = rdb.Session()
            mail.matched = True
            mail.match_on = datetime.now()
            session.add(mail)
            session.flush()

class AndCombination(RuleType, grok.GlobalUtility):
    """ XXX """
    grok.name('and')    
    name = 'mach all (and)'

    def apply(self, mails, rule):
        """ XXX """
        super(AndCombination, self).apply(mails, rule)
        executeMails = self.mails
        for filter in self.rule.getFilters():
            executeMails = filter.apply(executeMails)
        for action in self.rule.getActions():
            mtUtil = getUtility(IActionMatchType, action.match)
            mtUtil.apply(action, executeMails)
        self.markMatchedMails(executeMails)

class OrCombination(RuleType, grok.GlobalUtility):
    """ XXX """
    grok.name('or')    
    name = 'match any (or)'
    
    def apply(self, mails, rule):
        """ XXX """
        super(OrCombination, self).apply(mails, rule)
        executeMails = []
        for filter in self.rule.getFilters():
            executeMails.extend(filter.apply(self.mails))
        for action in self.rule.getActions():
            mtUtil = getUtility(IActionMatchType, action.match)
            mtUtil.apply(action, executeMails)
        self.markMatchedMails(executeMails)