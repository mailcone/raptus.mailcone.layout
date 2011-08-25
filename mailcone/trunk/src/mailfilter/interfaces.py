import grok

from zope import schema, interface
from zope.interface import Interface
from zope.schema.interfaces import IIterableSource
from zope.schema.vocabulary import SimpleTerm
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.browser.interfaces import ITerms
from zope.component import getUtility

class IMailfilterApp(Interface):
    """ XXX """
    title = schema.TextLine(title=u'Title', required=True)
    default_mail = schema.TextLine(title=u'Default mailaddress', required=False)
    
    def delRuleset(ruleset):
        """ 
            delete rule set from app folder
            param: customer contains id of to delete object 
        """
    
    def delCustomer(customer):
        """ 
            delete customer from app folder
            param: customer contains id of to delete object 
        """

class IDatabaseSettings(Interface):
    """ Interface define setting properties for database connection """
    driver = schema.TextLine(title=u'Driver', required=True)
#    user = schema.TextLine(title=u'User', required=False)
#    passwd = schema.Password(title=u'Password', required=False)
#    host = schema.TextLine(title=u'Host', required=True)
#    port = schema.TextLine(title=u'Port', required=True)
#    dbName = schema.TextLine(title=u'Database name', required=True)
        
class ISearchableContent(Interface):
    """ Interface for content models, contract used for indexing """
    content_type = interface.Attribute('content_type')
    id = interface.Attribute('id')
    parent_url = interface.Attribute('parent_url')
    implements = interface.Attribute('implements')
    sortNr = interface.Attribute('sortNr')

class IFilterMailsUtility(Interface):
    """ XXX - only for testing, must be moved maybe... - and if not renamed """

    def filterMails():
        """ XXX """

class ICopy(Interface):
    """ 
        Interface provide method to create a copy of the instance
        used to copy rule sets (templates) to a specific customer 
    """

    def copy(context):
        """ copy the instance to the given context - if childes provide ICopy they will copy too """

# XXX - should be renamed to IConfigletManager
class IControlPanel(Interface):
    """ Interface for control panel """
    
    def listConfiglets():
        """ return a list of dicts with the keys (title and url) for registered configlets """

# XXX - should be inherit from IControlPanel        
class ISettingConfigletManager(Interface):
    """ XXX """
    
    def listConfiglets():
        """ XXX """
        
class IRuleJSExtenerManager(Interface):
    """ XXX """
    
class IControlPanelJSExtention(Interface):
    """ XXX """
        
class IConfiglet(Interface):
    """ marker interface for a configlet """    

    # XXX - should also have attribute tab like ISettingConfiglet
    id = interface.Attribute('id')
    title = interface.Attribute('title')
    url = interface.Attribute('url')
    
class ISettingConfiglet(Interface):
    """ marker interface for a setting configlet """
    
    id = interface.Attribute('id')
    tab = interface.Attribute('tab')
    title = interface.Attribute('title')
    url = interface.Attribute('url')
    
class IFilterSettingConfiglet(Interface):
    """ Marker interface for filter setting configlet """
    
class IActionSettingConfiglet(Interface):
    """ Marker interface for filter setting configlet """

class IRuleContainer(Interface):
    """ Marker interface to provide rules as subcontents """

    rule_sort_nr = interface.Attribute('rule_sort_nr') 

    def addRule():
        """ XXX """
    
    def getNextRuleSortNr():
        """"XXX"""

    def getRules():
        """ return a list of contained rules """

    def moveRuleUp():
        """XXX"""
        
    def moveRuleDown():
        """XXX"""
        
    def delRule(rule):
        """ 
            delete rule from rule contaioner
            param: rule contains id of to delete object 
        """

class IRuleSet(Interface):
    """ Interface for rule set """
    id = schema.TextLine(title=u'id',required=True)
    name = schema.TextLine(title=u'name',required=True) #validate if id exists allready
    description = schema.Text(title=u'description', required=False)

class IPeriodUnit(Interface):
    """ XXX """
    name = interface.Attribute('name')

class IPeriodUnitManager(Interface):
    """ XXX """        

    def getUtilKeys():
        """ return keys of registered IPeriodUnit utilities """

    def getUtil(id):
        """ return util provides IPeriodUnit with id given as parameter """ 
    
class periodUnits(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(IPeriodUnitManager)
        return manager.getUtilKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class periodUnitsTerms(grok.MultiAdapter):
    grok.adapts(periodUnits, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(IPeriodUnitManager)
        util = manager.getUtil(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token
    
class ISeverity(Interface):
    """ XXX """
    name = interface.Attribute('name')

class ISeverityManager(Interface):
    """ XXX """        

    def getUtilKeys():
        """ return keys of registered ISeverity utilities """

    def getUtil(id):
        """ return util provides ISeverity with id given as parameter """
    
class Severities(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(ISeverityManager)
        return manager.getUtilKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class SeverityTerms(grok.MultiAdapter):
    grok.adapts(Severities, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(ISeverityManager)
        util = manager.getUtil(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token
    
class IRuleType(Interface):
    """ XXX """
    name = interface.Attribute('name')
    rule = interface.Attribute('rule')

    def apply(mails):
        """ XXX """

class IRuleTypeManager(Interface):
    """ XXX """        

    def getUtilKeys():
        """ return keys of registered IRuleType utilities """

    def getUtil(id):
        """ return util provides IRuleType with id given as parameter """
    
class RuleTypes(object):
    interface.implements(IIterableSource)
    
    def __init__(self):
        pass
    
    @property
    def _terms(self):
        manager = getUtility(IRuleTypeManager)
        return manager.getUtilKeys()

    def __iter__(self):
        return self._terms

    def __len__(self):
        return len(self._terms)
    
    def __contains__(self, value):
        return value in self._terms
    
class RuleTypeTerms(grok.MultiAdapter):
    grok.adapts(RuleTypes, IBrowserRequest)
    grok.provides(ITerms)
    
    def __init__(self, source, request):
        pass
    
    def getTerm(self, value):
        manager = getUtility(IRuleTypeManager)
        util = manager.getUtil(value) 
        return SimpleTerm(value, value, util.name)
        
    def getValue(self, token):
        return token

class IRule(Interface):
    """ Interface for rule set """
    id = schema.TextLine(title=u'id',required=True)
    last_modification = schema.Datetime(title=u'last modification', required=False)
    last_modi_user = schema.Set(title=u'last modification from user', required=False)
    #XXX - do not provide any logic at the moment
    #XXX - if match update match date
    last_match = schema.Datetime(title=u'last match', required=False)

    name = schema.TextLine(title=u'name',required=True) #validate if id exists allready
    description = schema.Text(title=u'description', required=False)
    severity = schema.Choice(title=u'severity',
                             source=Severities(),
                             required=True)
    matching = schema.Choice(title=u'matching',
                             source=RuleTypes(),
                             required=True)
    expect_mail = schema.Bool(title=u'expect mail', 
                              required=False)
    #XXX: zope.schema has a Field called Timedelta - have a look on it
    expect_period = schema.Int(title=u'expect mail period', 
                               required=False)
    expect_period_unit = schema.Choice(title=u'expect mail period unit',
                                       #XXX - must be utils 
                                       source=periodUnits(),
                                       required=False)
    #XXX - not shoure yet, if it is better to make own package for this feature
    testmail = schema.Text(title=u'test mail', required=False)

    #XXX - rename to sort_nr (contvention)
    sortNr = interface.Attribute('sortNr')
    
    def setSortNr():
        """ XXX """
    
    def setLastModificationUser():
        """ XXX """
    
    def getLastModificationUser():
        """ XXX """
    
    def setLastModificationDate():
        """ XXX """
    
    def getLastModificationDate():
        """ XXX """
        
    def apply(mails):
        """ XXX """

class ISmtpServerUtil(Interface):
    """ XXX """
    host = schema.TextLine(title=u'Host', required=True)
    email = schema.TextLine(title=u'Email address', required=True)
    authrequeried = schema.Bool(title=u'Authentication required', required=False)
    user = schema.TextLine(title=u'Smtp user', required=False)
    passwd = schema.Password(title=u'Password', required=False)

    def send(mail):
        """ send given mail obj over configured smtp host
        given mail must be a MIMEText object"""

class IBaseSettingObject(Interface):
    """ XXX """
    
    id = interface.Attribute('id')
    title = interface.Attribute('title')
    form_name = interface.Attribute('form_name')

    def getTitle():
        """ XXX """
    
    def getFormName():
        """ XXX """

class IActionSettingObject(IBaseSettingObject):
    """ XXX """

class IFilterSettingObject(IBaseSettingObject):
    """ XXX """