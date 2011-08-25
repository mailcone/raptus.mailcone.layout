import grok

class ViewMailfilter(grok.Permission):
    """ Permission allow simply the view of customers and their roles """
    grok.name('mailfilter.view')

class ManageRules(grok.Permission):
    """ Permission allow to manage rules """
    grok.name('mailfilter.manageRules')
    
class ViewControlpanel(grok.Permission):
    """ Permission allow the view of the control panel """
    grok.name('mailfilter.controlpanel')
    
class ManageCustomers(grok.Permission):
    """ Permission allow to manage customers """
    grok.name('mailfilter.manageCustomers')
    
class ManageRulesets(grok.Permission):
    """ Permission allow to manage rule sets """
    grok.name('mailfilter.manageRulesets')

# XXX - should be renamed to manageApp
class ManageUsers(grok.Permission):
    """ Permission allow to manage users """
    grok.name('mailfilter.manageUsers')