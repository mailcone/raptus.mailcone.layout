# grok stuff
import grok

# sql stuff
from megrok import rdb
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, String, Date, Text, Boolean
#XXX - could be change if provide by a util
from database_cfg import (create_metadata, skip_create_metadata)

from datetime import datetime

# zope stuff
from zope.component import getUtility
from zope.traversing.api import getPath
from zope import event, lifecycleevent

# catalog stuff
from hurry.query.interfaces import IQuery
from hurry.query import set, Eq, And

# mailfilter stuff
from mailfilter.app import MailfilterApp, SearchableContentMixin
from mailfilter.interfaces import (
    IRuleSet,
    IRuleType,
    IRule,
    IRuleContainer,
    ISearchableContent
)

from mfa_core_action.interfaces import IAction, IActionContainer 
from mfa_core_filter.interfaces import IFilter, IFilterContainer 

class RuleSet(grok.Container, SearchableContentMixin):
    """ Provide template container. Modeled rules can be easily copied to a customer afterwards """
    grok.implements(IRuleSet, IRuleContainer, ISearchableContent)
    grok.context(MailfilterApp)
    
    id = None
    sortNr = None # XXX - at the moment needed for index
    content_type = 'RuleSet'

    rule_sort_nr = 0

    def __init__(self, name, description):
        """ Constructor """
        super(RuleSet, self).__init__()
        self.id = name.lower().replace(' ', '_')
        self.name = name
        self.description = description

    def addRule(self, rule):
        """ add given filter object to the container """
        rule.setSortNr(self.getNextRuleSortNr())
        self[rule.id] = rule
        self.rule_sort_nr = self.rule_sort_nr + 1

    def getNextRuleSortNr(self):
        """ XXX """
        return self.rule_sort_nr

    def getRules(self):
        """ return a list of contained rules """
        query = getUtility(IQuery)
        return query.searchResults(set.AnyOf(('catalog', 'implements'), [IRule.__identifier__,]) & 
                                   Eq(('catalog', 'parent_url'), getPath(self)), 
                                   sort_field=('catalog', 'sortNr'))
    
    #XXX move up and down could be done by a Utility
    def moveRuleUp(self, obj):
        """ move rule given by obj one position up """
        
        if obj.sortNr != 0:
            # XXX make it with a query and index
            for rule in self.getRules():
                if rule.sortNr == obj.sortNr - 1:
                    rule.setSortNr(rule.sortNr + 1)
            
            obj.setSortNr(obj.sortNr - 1)
        
        return self
    
    def moveRuleDown(self, obj):
        """ move rule given by obj one position down """
        
        if obj.sortNr != (self.rule_sort_nr - 1):
            # XXX make it with a query and index
            for rule in self.getRules():
                if rule.sortNr == obj.sortNr + 1:
                    rule.setSortNr(rule.sortNr - 1)
            
            obj.setSortNr(obj.sortNr + 1)
        
        return self
    
    def _sortRulesNewBeforDel(self, sortNr):
        """ decrement rules with higher sort number """
        for rule in self.getRules():
            if rule.sortNr > sortNr:
                rule.setSortNr(rule.sortNr - 1)
    
    def delRule(self, rule):
        """ delete rule in current rule set """
        sortNr = rule.sortNr
        self._sortRulesNewBeforDel(sortNr) # all objects with higher sortNr are decremented
        self.rule_sort_nr = self.rule_sort_nr - 1
        del self[rule.__name__]
    
class Rule(grok.Container, SearchableContentMixin):
    """ Provide a container for filters and actions """
    grok.implements(IRule, ISearchableContent, IFilterContainer, IActionContainer)
    grok.context(IRuleContainer)

    id = None
    last_modification = None
    last_modi_user = None
    last_match = None
    content_type = 'Rule'
    next_id = 0
    expect_mail = False
    expect_period = None
    expect_period_unit = None
    testmail = None
    
    sortNr = None
    filter_sort_nr = 0
    action_sort_nr = 0

    def __init__(self, name, description, severity, matching, last_modi_user, expect_mail,
                 expect_period, expect_period_unit, testmail):
        """ Constructor """
        super(Rule, self).__init__()
        self.id = name.lower().replace(' ', '_')
        self.name = name
        self.description = description
        self.severity = severity
        self.matching = matching
        # XXX - should be done later in a Event IObjectCreatedEvent and IContainerModifiedEvent
        self.last_modification = datetime.now()
        self.last_modi_user = last_modi_user
        self.expect_mail = expect_mail
        self.expect_period = expect_period
        self.expect_period_unit = expect_period_unit
        self.testmail = testmail

    def setLastModificationUser(self, user):
        """ set last modification user """
        self.last_modi_user = user
    
    def getLastModificationUser(self):
        """ return last modification user """
        return self.last_modi_user.id

    def setLastModificationDate(self, date):
        """ set last modification date """
        self.last_modification = date
    
    def getLastModificationDate(self):
        """ return last modification date """
        # should be managable over configlet
        return self.last_modification.strftime("%d.%m.%y %H:%M")

    grok.traversable('moveUp')
    def moveUp(self):
        """ XXX """
        return self.__parent__.moveRuleUp(self)

    grok.traversable('moveDown')
    def moveDown(self):
        """ XXX """
        return self.__parent__.moveRuleDown(self)

    def setSortNr(self, number):
        """ set sort number - given by rule container """
        self.sortNr = number
        #reindexing
        event.notify(lifecycleevent.ObjectModifiedEvent(self, lifecycleevent.Attributes(IRule, 'sortNr')))

    def getNextId(self):
        """ return the next free 'numeric' id as a string """
        return str(self.next_id)
        
    def getNextFilterSortNr(self):
        """ return next free sort number """
        return self.filter_sort_nr
    
    def addFilter(self, filter):
        """ add given filter object to the container """
        filter.setSortNr(self.getNextFilterSortNr())
        self[filter.id] = filter
        self.next_id = self.next_id + 1
        self.filter_sort_nr = self.filter_sort_nr + 1
    
    def getFilters(self):
        """ return a list of contained filters """
        query = getUtility(IQuery)
        return query.searchResults(set.AnyOf(('catalog', 'implements'), [IFilter.__identifier__,]) & 
                                   Eq(('catalog', 'parent_url'), getPath(self)),
                                   sort_field=('catalog', 'sortNr'))
    
    
    def _sortFiltersNewBeforDel(self, sortNr):
        """ decrement filter with higher sort number """
        for filter in self.getFilters():
            if filter.sortNr > sortNr:
                filter.setSortNr(filter.sortNr - 1)
    
    #XXX move up and down could be done by a Utility
    def moveFilterUp(self, obj):
        """ move filter given by obj one position up """
        
        if obj.sortNr != 0:
            # XXX make it with a query and index
            for filter in self.getFilters():
                if filter.sortNr == obj.sortNr - 1:
                    filter.setSortNr(filter.sortNr + 1)
            
            obj.setSortNr(obj.sortNr - 1)
        
        return self
    
    def moveFilterDown(self, obj):
        """ move filter given by obj one position down """
        
        if obj.sortNr != (self.filter_sort_nr - 1):
            # XXX make it with a query and index
            for filter in self.getFilters():
                if filter.sortNr == obj.sortNr + 1:
                    filter.setSortNr(filter.sortNr - 1)
            
            obj.setSortNr(obj.sortNr + 1)
        
        return self
    
    def delFilter(self, filter):
        """ delete filter in current rule """
        sortNr = filter.sortNr
        self._sortFiltersNewBeforDel(sortNr) # all objects with higher sortNr are decremented
        self.filter_sort_nr = self.filter_sort_nr - 1
        del self[filter.__name__]

    def getNextActionSortNr(self):
        """ XXX """
        return self.action_sort_nr

    def addAction(self, action):
        """ add given action object to the container """
        action.setSortNr(self.getNextActionSortNr())
        self[action.id] = action
        self.next_id = self.next_id + 1
        self.action_sort_nr = self.action_sort_nr + 1
        
    def getActions(self):
        """ return a list of contained filters """
        query = getUtility(IQuery)
        return query.searchResults(set.AnyOf(('catalog', 'implements'), [IAction.__identifier__,]) & 
                                   Eq(('catalog', 'parent_url'), getPath(self)),
                                   sort_field=('catalog', 'sortNr'))

    #XXX move up and down could be done by a Utility
    def moveActionUp(self, obj):
        """ move action given by obj one position up """
        
        if obj.sortNr != 0:
            # XXX make it with a query and index
            for action in self.getActions():
                if action.sortNr == obj.sortNr - 1:
                    action.setSortNr(action.sortNr + 1)
            
            obj.setSortNr(obj.sortNr - 1)
        
        return self
    
    def moveActionDown(self, obj):
        """ move action given by obj one position down """
        
        if obj.sortNr != (self.action_sort_nr - 1):
            # XXX make it with a query and index
            for action in self.getActions():
                if action.sortNr == obj.sortNr + 1:
                    action.setSortNr(action.sortNr - 1)
            
            obj.setSortNr(obj.sortNr + 1)
        
        return self

    def _sortActionsNewBeforDel(self, sortNr):
        """ decrement action with higher sort number """
        for action in self.getActions():
            if action.sortNr > sortNr:
                action.setSortNr(action.sortNr - 1)
        
    def delAction(self, action):
        """ delete action in current rule """
        sortNr = action.sortNr
        self._sortActionsNewBeforDel(sortNr) # all objects with higher sortNr are decremented
        self.action_sort_nr = self.action_sort_nr - 1
        del self[action.__name__]
        
    def apply(self, mails):
        """ apply rule on given source - at the moment only mails
            first step: walk through filters
            second step: apply action based on match result get back by filters
        """
        ruleTypeUtil = getUtility(IRuleType, self.matching)
        matchType = ruleTypeUtil.apply(mails, self)
            
        #XXX update last match
        
class Mail(rdb.Model):
    """ Model for mails """
    rdb.metadata(create_metadata)
    rdb.tablename('mail') #XXX - should be configurable
    
    id = Column ('id', Integer, Sequence('mail_id_seq'), primary_key=True)
    date = Column ('date', Date)
    mail_from = Column ('mail_from', String(250))
    mail_from_domain = Column ('mail_from_domain', String(250))
    organisation = Column ('organisation', String(250))
    mail_to = Column ('mail_to', Text)
    mail_to_domain = Column ('mail_to_domain', Text)
    mail_cc = Column ('mail_cc', Text)
    in_reply_to = Column ('in_reply_to', Text)
    mail_references = Column ('mail_references', Text)
    header = Column ('header', Text)
    subject = Column ('subject', String(250))
    content = Column ('content', Text)
    path_to_attachments = Column ('path_to_attachments', Text)
    matched = Column('matched', Boolean)
    match_on = Column ('match_on', Date)