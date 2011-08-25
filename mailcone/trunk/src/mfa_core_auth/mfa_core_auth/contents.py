import grok

from zope.component import getUtility
from zope.password.interfaces import IPasswordManager
from zope.pluggableauth.interfaces import IPrincipalInfo

from mfa_core_auth.interfaces import IAccount

class PrincipalInfo(object):
    """XXX"""
    grok.implements(IPrincipalInfo)

    def __init__(self, id, title, description):
        """ Constructor """
        self.id = id
        self.title = title
        self.description = description
        self.credentialsPlugin = None
        self.authenticatorPlugin = None

class UserFolder(grok.Container):
    """XXX"""
    
    def __init__(self, title):
        """ Constructor """
        super(UserFolder, self).__init__()
        self.title = title

class Account(grok.Model):
    """XXX"""
    grok.implements(IAccount)
    
    def __init__(self, name, password, real_name, role):
        """ Constructor """
        super(Account, self).__init__()
        #XXX - title just for test - is at the moment needed, otherwise head.pt failed
        self.title = name
        self.name = name
        self.real_name = real_name
        self.role = role
        self.setPassword(password)

    def setPassword(self, password):
        """XXX"""
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        self.password = passwordmanager.encodePassword(password)

    def checkPassword(self, password):
        """XXX"""
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        return passwordmanager.checkPassword(self.password, password)