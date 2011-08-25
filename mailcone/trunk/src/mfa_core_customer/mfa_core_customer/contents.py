# grok stuff
import grok

# zope stuff
from zope.component import getUtility
from zope.traversing.api import getPath

# catalog stuff
from hurry.query.interfaces import IQuery
from hurry.query import set, Eq

from mailfilter.interfaces import IRuleContainer, IRule, ISearchableContent
from mfa_core_customer.interfaces import ICustomer

# mailfilter stuff
from mailfilter.app import MailfilterApp, SearchableContentMixin

class Customer(grok.Container):
    """ Provide a container for customer specific rules """
    grok.context(MailfilterApp)
    grok.implements(ICustomer, IRuleContainer, ISearchableContent)
    
    id = None
    sortNr = None # XXX - at the moment needed for index
    content_type = 'Customer'
    
    rule_sort_nr = 0
    
    def __init__(self, name, address):
        """ Constructor """
        super(Customer, self).__init__()
        self.id = name.lower().replace(' ', '_')
        self.name = name
        self.address = address

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
        """ decrement action with higher sort number """
        for rule in self.getRules():
            if rule.sortNr > sortNr:
                rule.setSortNr(rule.sortNr - 1)

    def delRule(self, rule):
        """ delete rule in current rule set """
        sortNr = rule.sortNr
        self._sortRulesNewBeforDel(sortNr) # all objects with higher sortNr are decremented
        self.rule_sort_nr = self.rule_sort_nr - 1
        del self[rule.__name__]