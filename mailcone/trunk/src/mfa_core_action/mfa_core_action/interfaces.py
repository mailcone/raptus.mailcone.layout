import grok

from zope import schema, interface
from zope.interface import Interface
from zope.schema.interfaces import IIterableSource
from zope.schema.vocabulary import SimpleTerm
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.browser.interfaces import ITerms
from zope.component import getUtility

class IAction(Interface):
    """ Interface for action """
    
    # when ISortable is implemented not needed anymore
    sortNr = interface.Attribute('sortNr')
    
    def setSortNr():
        """ set sort number used by action container """

    def getActionTypeTitle():
        """ return action type """

    def apply():
        """ XXX """
    
class IActionType(Interface):
    """ Interface for action type """
    title = interface.Attribute('title')
    addFormName = interface.Attribute('addFormName')
    
    def getSettingObject(self):
        """ XXX """
    
    # XXX - start here - setting must be defined and create if not there

class IActionContainer(Interface):
    """ Marker interface to provide action as subcontents """

    next_id = interface.Attribute('next_id')
    
    def getNextId():
        """ return next available nummeric id - return id as string"""

    def getNextActionSortNr():
        """ return next nummeric id for actions """

    def addAction(action):
        """ add new action to container """
    
    def getActions():
        """ return a list of contained actions """
        
    def moveActionUp(obj):
        """ move action one position up """

    def moveActionDown(obj):
        """ move action one position down """
    
    def delAction(action):
        """ 
            delete filter from filter container
            param: filter contains id of to delete object
        """

class IActionManager(Interface):
    """ Interface for action manager """
    
    def listActionTypes(context):
        """ 
            return a dict of all registered filterType utils - dict provides keys 
            (title and url), the context must be a view object
        """
    
    def listActionSettings(self):
        """ XXX """

class IActionMatchType(Interface):
    """ Interface for match types """
    name = interface.Attribute('name')
    
    def apply(action, resultMails):
        """ XXX """
        
class IActionMatchTypeManager(Interface):
    """ Interface for match types manager """
    
    def getUtilKeys():
        """ return keys of registered IActionMatchType utilities """

    def getUtil(id):
        """ return util provides IActionMatchType with id given as parameter """
        
class ActionMatchTypes(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(IActionMatchTypeManager)
        return manager.getUtilKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class ActionMatchTypesTerms(grok.MultiAdapter):
    grok.adapts(ActionMatchTypes, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(IActionMatchTypeManager)
        util = manager.getUtil(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token
    
class IActionSettings(Interface):
    """ XXX - not finished yet """
    
class IActionSettingsManager(Interface):
    """ XXX - not finished yet """