from zope.interface import Interface
from zope import interface, schema

class ICustomer(Interface):
    """ Interface for customer """
    id = schema.TextLine(title=u'id', required=True)
    name = schema.TextLine(title=u'name', required=True)
    address = schema.Text(title=u'address', required=True)