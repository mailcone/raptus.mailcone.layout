import grok

from zope.component import getUtility
from zope import event, lifecycleevent

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import ISearchableContent
from mfa_core_filter.interfaces import (
    IFilter, 
    IFilterType, 
    IFilterContainer,
    IMailSourceManager,
    ISimpleFilterOperatorManager
) 
from mfa_simplematchfilter.interfaces import ISimpleMatchFilter

class SimpleMatchFilter(grok.Model, SearchableContentMixin):
    """ Provide a filter for string conditions filtered by an operator """
    grok.implements(ISimpleMatchFilter, IFilter, ISearchableContent)
    grok.context(IFilterContainer)
    
    id = None
    content_type = 'SimpleMatchFilter'
    sortNr = None

    def __init__(self, id, source, operator, condition):
        """ Constructor """
        super(SimpleMatchFilter, self).__init__()
        self.id = id
        self.source = source
        self.operator = operator
        self.condition = condition

    def setSortNr(self, number):
        """XXX"""
        self.sortNr = number
        #reindexing
        event.notify(
            lifecycleevent.ObjectModifiedEvent(self, 
                                               lifecycleevent.Attributes(ISimpleMatchFilter, 'sortNr')
            )
        )
        
    grok.traversable('moveUp')
    def moveUp(self):
        return self.__parent__.moveFilterUp(self)

    grok.traversable('moveDown')
    def moveDown(self):
        return self.__parent__.moveFilterDown(self)

    def getFilterTypeTitle(self):
        """ return title for registered filter type """
        return getUtility(IFilterType, "SimpleMatchFilterType").title

    def apply(self, executeMails):
        """ XXX """
        filteredMails = []
        codeLines = []
        for mail in executeMails:
            sourceManager = getUtility(IMailSourceManager)
            source = sourceManager.getSource(self.source, mail)
            operatorManager = getUtility(ISimpleFilterOperatorManager)
            if operatorManager.apply(self.operator, self.condition, source):
                filteredMails.append(mail)
        return filteredMails