import grok

class LowEmployee(grok.Role):
    """ Role give an employee the rights to manage rule sets and customer specific rules """
    grok.name('mailfilter.LowEmployee')
    grok.permissions('mailfilter.view','mailfilter.manageRules')

class HighEmployee(grok.Role):
    """ Role contains same permission as low employee but has additional the permission 
        to manage customers """
    grok.name('mailfilter.HighEmployee')
    grok.permissions('mailfilter.view',
                     'mailfilter.manageRules', 
                     'mailfilter.controlpanel',
                     'mailfilter.manageRulesets', 
                     'mailfilter.manageCustomers')
    
class AppManager(grok.Role):
    """ Role has all permissions on the app. Roles (AppManager and HightEmployee) 
        vary in permission to manage users. """
    grok.name('mailfilter.AppManager')
    grok.permissions('mailfilter.view',
                     'mailfilter.manageRules', 
                     'mailfilter.controlpanel', 
                     'mailfilter.manageCustomers',
                     'mailfilter.manageRulesets',
                     'mailfilter.manageUsers')
