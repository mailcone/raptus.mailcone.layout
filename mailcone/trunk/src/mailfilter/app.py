# grok stuff
import grok
from zope import component
from zope.traversing.api import getPath
from zope.component import getUtility

from mailfilter.smtpUtil import SmtpServerUtil
from mailfilter.configlets import FilterSettingConfiglet, ActionSettingConfiglet
from mailfilter.interfaces import (
    IMailfilterApp, 
    ISmtpServerUtil,
    ISettingConfiglet
)
from mailfilter import resource

from zope.pluggableauth.authentication import PluggableAuthentication
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from mfa_core_auth.auth import setup_authentication
from mfa_core_auth.utils import UserAuthenticatorPlugin

class MailfilterApp(grok.Application, grok.Container):
    grok.implements(IMailfilterApp)
    
    grok.local_utility(
        UserAuthenticatorPlugin, provides=IAuthenticatorPlugin,
        name='users',
        )
    grok.local_utility(
        PluggableAuthentication, provides=IAuthentication,
        setup=setup_authentication,
        )
    grok.local_utility(SmtpServerUtil, provides=ISmtpServerUtil)
    grok.local_utility(FilterSettingConfiglet, 
                       provides=ISettingConfiglet, 
                       name='FilterSettings')
    grok.local_utility(ActionSettingConfiglet, 
                       provides=ISettingConfiglet, 
                       name='ActionSettings')
    
    title = None
    default_mail = None
    
    def __init__(self):
        """ Constructor """
        super(MailfilterApp, self).__init__()
        #at the moment hard coded, if app upgrade may be change
        self.title = 'Mailfilter'
    
    def delRuleset(self, ruleset):
        del self[ruleset]
    
    def delCustomer(self, customer):
        del self[customer]
    
    grok.traversable('smtpSettings')
    def smtpSettings(self):
        return getUtility(ISmtpServerUtil)

    grok.traversable('filterSettings')
    def filterSettings(self):
        return getUtility(ISettingConfiglet, 'FilterSettings')
    
    grok.traversable('actionSettings')
    def actionSettings(self):
        return getUtility(ISettingConfiglet, 'ActionSettings')
        
    grok.traversable('userConfiglet')
    def userConfiglet(self):
        return component.getUtility(IAuthenticatorPlugin,'users').user_folder

class SearchableContentMixin:
    """
        Mixin class for objects implementing the SearchableContent interface
    """
    
    @property
    def implements(self):
        """ return a list with all defined interfaces for the object """
        return [i.__identifier__ for i in self.__provides__.interfaces()]
    
    @property
    def parent_url(self):
        """ return the path of the object """
        return getPath(self.__parent__)