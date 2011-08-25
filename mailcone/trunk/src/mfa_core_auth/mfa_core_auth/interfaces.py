from zope import schema 
from zope.interface import Interface

class ILoginForm(Interface):
    """XXX"""
    login = schema.BytesLine(title=u'Username', required=True)
    camefrom = schema.BytesLine(title=u'', required=False)
    password = schema.Password(title=u'Password', required=True)

class IAccount(Interface):
    """XXX"""
    name = schema.BytesLine(title=u'Username', required=True)
    password = schema.Password(title=u'Password', required=True)
    real_name = schema.BytesLine(title=u'Real name', required=True)
    role = schema.Choice(title=u'User role',
                         values=[u'Low employee', u'High employee', u'Application Manager'],
                         required=True)

class IAddUserForm(Interface):
    """XXX"""
    login = schema.BytesLine(title=u'Username', required=True)
    password = schema.Password(title=u'Password', required=True)
    confirm_password = schema.Password(title=u'Confirm password', required=True)
    real_name = schema.BytesLine(title=u'Real name', required=True)
    role = schema.Choice(title=u'User role',
                         values=[u'Low employee', u'High employee', u'Application Manager'],
                         required=True)
    