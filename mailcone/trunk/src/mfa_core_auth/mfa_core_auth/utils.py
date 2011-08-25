import grok

from zope.pluggableauth.plugins.session import SessionCredentialsPlugin
from zope.pluggableauth.interfaces import ICredentialsPlugin
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.securitypolicy.interfaces import IPrincipalRoleManager

from mfa_core_auth.contents import UserFolder, PrincipalInfo, Account

class MySessionCredentialsPlugin(grok.GlobalUtility, SessionCredentialsPlugin):
    """XXX"""
    grok.provides(ICredentialsPlugin)
    grok.name('credentials')

    loginpagename = 'login'
    loginfield = 'login'
    passwordfield = 'password'

class UserAuthenticatorPlugin(grok.LocalUtility):
    """XXX"""
    grok.implements(IAuthenticatorPlugin)
    grok.name('users')

    def __init__(self):
        """ Constructor """
        self.user_folder = UserFolder('users')
        
    def authenticateCredentials(self, credentials):
        """XXX"""
        if not isinstance(credentials, dict):
            return None
        if not ('login' in credentials and 'password' in credentials):
            return None
        account = self.getAccount(credentials['login'])

        if account is None:
            return None
        if not account.checkPassword(credentials['password']):
            return None
        return PrincipalInfo(id=account.name,
                             title=account.real_name,
                             description=account.real_name)

    def principalInfo(self, id):
        """XXX"""
        account = self.getAccount(id)
        if account is None:
            return None
        return PrincipalInfo(id=account.name,
                             title=account.real_name,
                             description=account.real_name)

    def getAccount(self, login):
        """XXX"""
        return login in self.user_folder and self.user_folder[login] or None
    
    def addUser(self, username, password, real_name, role):
        """XXX"""
        if username not in self.user_folder:
            user = Account(username, password, real_name, role)
            self.user_folder[username] = user
            role_manager = IPrincipalRoleManager(grok.getSite())
            if role==u'High employee':
                role_manager.assignRoleToPrincipal('mailfilter.HighEmployee',username)
            elif role==u'Application Manager':
                role_manager.assignRoleToPrincipal('mailfilter.AppManager',username)
            else:
                role_manager.assignRoleToPrincipal('mailfilter.LowEmployee',username)
            
    def listUsers(self):
        """XXX"""
        return self.user_folder.values()