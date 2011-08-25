import grok
import re

from zope.component import getUtility
from zope import event, lifecycleevent

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import ISearchableContent
from mfa_core_filter.interfaces import IFilter, IFilterType, IFilterContainer, IMailSourceManager
from mfa_complexmatchfilter.interfaces import IComplexMatchFilter


class ComplexMatchFilter(grok.Model, SearchableContentMixin):
    """ Provide a filter for regular expressions """
    grok.implements(IComplexMatchFilter, IFilter, ISearchableContent)
    grok.context(IFilterContainer)

    id = None
    content_type = 'ComplexMatchFilter'
    sortNr = None

    def __init__(self, id, source, condition):
        """ Constructor """
        super(ComplexMatchFilter, self).__init__()
        self.id = id
        self.source = source
        self.condition = condition

    def setSortNr(self, number):
        """XXX"""
        self.sortNr = number
        #reindexing
        event.notify(
            lifecycleevent.ObjectModifiedEvent(self, 
                                               lifecycleevent.Attributes(IComplexMatchFilter, 'sortNr')
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
        return getUtility(IFilterType, "ComplexMatchFilterType").title

    def apply(self, executeMails):
        """ XXX """
        filteredMails = []
        for mail in executeMails:
            sourceManager = getUtility(IMailSourceManager)
            source = sourceManager.getSource(self.source, mail)
            if re.search (self.condition, source.strip()):
                filteredMails.append(mail)
        return filteredMails