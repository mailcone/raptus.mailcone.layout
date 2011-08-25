import grok

from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter

# catalog stuff
from hurry.query.interfaces import IQuery
from hurry.query import Eq

from mailfilter.app import MailfilterApp
from mailfilter.viewletmanagers import Main
from mailfilter.interfaces import IRuleJSExtenerManager, ICopy
from mailfilter.resource import controlPanelCss, controlPanelJs
from mailfilter.resource import library as MailfilterLibrary

from mfa_core_customer.interfaces import ICustomer
from mfa_core_customer.contents import Customer
from mfa_core_customer.resource import popupCss, popupJs

#
# Configlet
#
class CustomerConfigletView (grok.View):
    """ Provide view for customer management """
    grok.context(MailfilterApp)
    grok.name('customerConfiglet')
    grok.template('master')
    grok.require('mailfilter.view')

class CustomerConfigletViewlet(grok.Viewlet):
    """ XXX """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('customer_configlet')
    grok.view(CustomerConfigletView)

    customers = None

    def _getCustomers(self):
        """ return a list of all existing customer instances """
        query = getUtility(IQuery)
        return query.searchResults(Eq(('catalog', 'content_type'), 'Customer'))

    def update(self):
        self.customers = self._getCustomers()

#
# Customer
#        
class CustomerMacro(grok.View):
    """ used for control panel to display customer informations """
    grok.context(ICustomer)
    grok.template('customer_macro')
    grok.name('macro')
    grok.require('mailfilter.view')

class CpCustomerView(grok.View):
    """ XXX """
    grok.context(ICustomer)
    grok.template('master')
    grok.name('controlpanel_view')
    grok.require('mailfilter.view')

class CpCustomerViewlet(grok.Viewlet):
    """ XXX"""
    grok.viewletmanager(Main)
    grok.context(ICustomer)
    grok.template('customer_controlpanel_viewlet')
    grok.view(CpCustomerView)

class CustomerView(grok.View):
    """ Provide main view for a customer object """
    grok.context(ICustomer)
    grok.template('master')
    grok.name('index')
    grok.require('mailfilter.view')
    
class CustomerViewlet(grok.Viewlet):
    """ Provide viewlet for CustomerView """
    grok.viewletmanager(Main)
    grok.context(ICustomer)
    grok.template('customer_viewlet')
    grok.view(CustomerView)

    def update(self):
        controlPanelCss.need()
        controlPanelJs.need()
        popupCss.need()
        popupJs.need()
        # register js scripts needed for ajax
        jsExManager = getUtility(IRuleJSExtenerManager)
        for jsExtension in jsExManager.listJSExtensions():
            jsExtension.need()

class AddCustomerView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(MailfilterApp)
    grok.template('master')
    grok.name('addCustomer')
    grok.require('mailfilter.view')

    def getActionButtonId(self):
        return 'addCustomerButton'

    def getAction(self):
        return 'add'

    def update(self):
        if self.request.method == 'POST':
            name = self.request.get('name')
            address = self.request.get('address')
            
            obj = Customer(name, address)
            self.context[obj.id] = obj
            self.redirect(self.url(obj, 'controlpanel_view'))

class AddCustomerViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddCustomerForm """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('add_customer_viewlet')
    grok.view(AddCustomerView)

class EditCustomerView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(ICustomer)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')
    
    def getActionButtonId(self):
        return 'editCustomerButton'
    
    def getAction(self):
        return 'save'
    
    def update(self):
        if self.request.method == "POST":
            self.context.name = self.request.get('name')
            self.context.address = self.request.get('address')
            self.redirect(self.url(self.context, 'controlpanel_view'))

class EditCustomerViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditCustomerForm """
    grok.viewletmanager(Main)
    grok.context(ICustomer)
    grok.template('add_customer_viewlet')
    grok.view(EditCustomerView)

class DeleteCustomerView(grok.View):
    """ XXX """
    grok.context(ICustomer)
    grok.name('delete')
    grok.require('mailfilter.view')

    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delCustomer(self.context.__name__)
    
    def render(self):
        self.redirect(self.url(self.parent, 'customerConfiglet'))

class LoadRuleSetView(grok.View):
    """ Povide a view to load defined rule sets for a customer """
    grok.context(ICustomer)
    grok.name('loadRuleSet')
    grok.template('master')
    grok.require('mailfilter.view')

    rulesets = None
    
    def _getRuleSets(self):
        """ return a list of all existing rule set instances """
        query = getUtility(IQuery)
        return query.searchResults(Eq(('catalog', 'content_type'), 'RuleSet'))
    
    def update(self):
        self.rulesets = self._getRuleSets()
        if self.request.method == 'POST':
            for ruleset in self.rulesets: 
                selectSpecificRules = False
                if self.request.get(ruleset.id):
                    for rule in ruleset.getRules():
                        # if specific rule is selected only they are copied
                        if self.request.get(rule.id):
                            # XXX should be in customer content
                            ICopy(rule).copy(self.context)
                            selectSpecificRules = True
                    if selectSpecificRules == False:
                        # if no specific rule is selected all rules of rule set will be copied
                        for rule in ruleset.getRules():
                            ICopy(rule).copy(self.context)
            self.redirect(self.url('index'))

class LoadRuleSetViewlet(grok.Viewlet):
    """ Viewlet for LoadRuleSetView """
    grok.viewletmanager(Main)
    grok.context(ICustomer)
    grok.template('load_ruleset_viewlet')
    grok.view(LoadRuleSetView)