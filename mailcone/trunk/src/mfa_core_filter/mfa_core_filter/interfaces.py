import grok

from zope.interface import Interface
from zope import interface, schema 
from zope.schema.interfaces import IIterableSource
from zope.schema.vocabulary import SimpleTerm
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.browser.interfaces import ITerms
from zope.component import getUtility

class IFilter(Interface):
    """ Interface for filter """
    
    # when ISortable is implemented not needed anymore
    #XXX - rename to sort_nr (contvention)
    sortNr = interface.Attribute('sortNr')
    
    def setSortNr():
        """ set sort number used by filter container """
    
    def getFilterTypeTitle():
        """ return filter type """

    def apply(executeMails):
        """ XXX 
            param: executeMails - working copy of mails"""

class IFilterType(Interface):
    """ Interface for filter type """
    title = interface.Attribute('title')
    addFormName = interface.Attribute('addFormName')

class IFilterContainer(Interface):
    """ Marker interface to provide filter as subcontents """
    
    next_id = interface.Attribute('next_id')
    filter_sort_nr = interface.Attribute('filter_sort_nr')
    
    def getNextId():
        """ return next available nummeric id - return id as string"""

    def getNextFilterSortNr():
        """ return next nummeric id for filters """

    def addFilter(filter):
        """ add new filter to container """
    
    def getFilters():
        """ return a list of contained filters """

    def moveFilterUp(obj):
        """ move action one position up """

    def moveFilterDown(obj):
        """ move filter one position down """
    
    def delFilter(filter):
        """ 
            delete filter from filter container
            param: filter contains id of to delete object
        """

class IFilterManager(Interface):
    """ Interface for filter manager """
    
    def listFilterTypes(self, context):
        """ 
            return a dict of all registered filterType utils - dict provides keys 
            (title and url), the given context must be a view object 
        """
        
    def listFilterSettings(self):
        """ XXX """

class ISimpleFilterOperator(Interface):
    """ XXX """
    
    name = interface.Attribute('name')
    
    def apply(condition, source):
        """ XXX """
    
class ISimpleFilterOperatorOperationBased(ISimpleFilterOperator):
    """ XXX """

class ISimpleFilterOperatorFuncBased(ISimpleFilterOperator):
    """ XXX """
    
    funcName = interface.Attribute('funcName')
    
class ISimpleFilterOperatorManager(Interface):
    """ Interface for simple filter operators manager """
    
    def getSourceKeys():
        """ return keys of registered ISimpleFilterOperator utilities """

    def getSource(id):
        """ return util provides ISimpleFilterOperator with id given as parameter """
        
    def apply(operator, source, condition):
        """ XXX """

class SimpleFilterOperators(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(ISimpleFilterOperatorManager)
        return manager.getSourceKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms

class SimpleFilterOperaterTerms(grok.MultiAdapter):
    grok.adapts(SimpleFilterOperators, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(ISimpleFilterOperatorManager)
        source = manager.getSource(value) 
        return SimpleTerm(value, value, source.name)
        
    def getValue(self, token):
        return token

#XXX all mail move to mfa_core_mail
class IMailSource(Interface):
    """ XXX """
    name = interface.Attribute('name')
    attrName = interface.Attribute('source')
    
    def getSource(obj):
        """ XXX """

class IMailSourceManager(Interface):
    """ XXX """
    
    def getSourceKeys():
        """ return keys of registered IMailSource utilities """
    
    def getSourceUtil(id):
        """ return util provides IMailSource with id given as parameter """
    
    def getSource(id, obj):
        """ XXX """
    
class MailSources(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(IMailSourceManager)
        return manager.getSourceKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms

class MailTerms(grok.MultiAdapter):
    grok.adapts(MailSources, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        mailSourceManager = getUtility(IMailSourceManager)
        source = mailSourceManager.getSourceUtil(value) 
        return SimpleTerm(value, value, source.name)
        
    def getValue(self, token):
        return token

class IFilterSettings(Interface):
    """ XXX - not finished yet """
    
class IFilterSettingsManager(Interface):
    """ XXX - not finished yet """