# grok stuff
import grok

from mailfilter.interfaces import (
    IConfiglet, 
    ISettingConfiglet, 
    IFilterSettingConfiglet, 
    IActionSettingConfiglet
)

class RuleSetConfiglet(grok.GlobalUtility):
    """ Utility provide a gui to manage rule sets """
    grok.implements(IConfiglet)
    grok.name('RuleSetConfiglet')

    id = 'RuleSetConfiglet' # defines link id
    title = 'rule sets' # defines link content
    url = 'rulesetConfiglet'

#XXX move to mfa_core_auth
class UserConfiglet(grok.GlobalUtility):
    """ Utility provide a gui to manage users """
    grok.implements(IConfiglet)
    grok.name('UserConfiglet')

    id = 'UserConfiglet' # defines link id
    title = 'users' # defines link content
    url = 'userConfiglet'

# XXX - should be renamed to SettingConfiglet
class AppConfiglet(grok.GlobalUtility):
    """ Utility provide a gui to manage users """
    grok.implements(IConfiglet)
    grok.name('AppConfiglet')

    id = 'AppConfiglet' # defines link id
    title = 'settings' # defines link content
    url = 'appConfiglet'
    
class AppSettingConfiglet(grok.GlobalUtility):
    """ XXX """
    grok.implements(ISettingConfiglet)
    grok.name('AppSettings')
    
    id = 'AppSettings' # defines link id
    tab = 'app' # defines link content
    title = 'App settings'
    url = 'appSettings'

class DatabaseSettingConfiglet(grok.GlobalUtility):
    """ XXX """
    grok.implements(ISettingConfiglet)
    grok.name('DatabaseSettings')
    
    id = 'DatabaseSettings' # defines link id
    tab = 'database' # defines link content
    title = 'Database settings'
    url = 'databaseSettings'

class SmtpSettingConfiglet(grok.GlobalUtility):
    """ XXX """
    grok.implements(ISettingConfiglet)
    grok.name('SmtpSettings')
    
    id = 'SmtpSettings' # defines link id
    tab = 'smtp' # defines link content
    title = 'Smpt server settings'
    url = 'smtpSettings'

#XXX - should be moved to mfa_core_filter
class FilterSettingConfiglet(grok.LocalUtility):
    """ XXX """
    grok.implements(IFilterSettingConfiglet, ISettingConfiglet)
    grok.provides(ISettingConfiglet)
    grok.name('FilterSettings')
    
    id = 'FilterSettings' # defines link id
    tab = 'filters'
    title = 'Filter settings' # defines link content
    url = 'filterSettings'

#XXX - should be moved to mfa_core_action    
class ActionSettingConfiglet(grok.LocalUtility):
    """ XXX """
    grok.implements(IActionSettingConfiglet, ISettingConfiglet)
    grok.provides(ISettingConfiglet)
    grok.name('ActionSettings')
    
    id = 'ActionSettings' # defines link id
    tab = 'actions' # defines link content
    title = 'Action settings'
    url = 'actionSettings'