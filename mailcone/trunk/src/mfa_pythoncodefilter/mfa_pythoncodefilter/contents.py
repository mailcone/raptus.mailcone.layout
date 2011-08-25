import grok

from zope.component import getUtility
from zope import event, lifecycleevent

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import ISearchableContent
from mfa_core_filter.interfaces import IFilter, IFilterType, IFilterContainer
from mfa_pythoncodefilter.interfaces import IPythonCodeFilter

class PythonCodeFilter(grok.Model, SearchableContentMixin):
    """ Provide a filter declared by own python code """
    grok.implements(IPythonCodeFilter, IFilter, ISearchableContent)
    grok.context(IFilterContainer)

    id = None
    content_type = 'PythonCodeFilter'
    sortNr = None

    def __init__(self, id, code):
        """ Constructor """
        super(PythonCodeFilter, self).__init__()
        self.id = id
        self.code = code

    def setSortNr(self, number):
        """XXX"""
        self.sortNr = number
        #reindexing
        event.notify(
            lifecycleevent.ObjectModifiedEvent(self, 
                                               lifecycleevent.Attributes(IPythonCodeFilter, 'sortNr')
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
        return getUtility(IFilterType, "PythonCodeFilterType").title
    
    def apply(self, executeMails):
        """ XXX """
        filteredMails = []
        code = self.code
        
        # XXX - not finished - think there is a better solution
        variables = {'header': 'mail.header', 
                     'from':'mail.mail_from',
                     'from_dom':'mail.mail_from_domain',
                     'to':'mail.mail_to',
                     'to_dom':'mail.mail_to_domain', 
                     'match':'match'}

        # replace place holders in code with variables
        for key, val in variables.items():
            var = '${' + key + '}'
            code = code.replace(var, val)
        
        # execute python code on each mail and 
        # append it to filteredMails if match    
        for mail in executeMails:
            match = False
            exec(code)
            if match:
                filteredMails.append(mail)

        return filteredMails