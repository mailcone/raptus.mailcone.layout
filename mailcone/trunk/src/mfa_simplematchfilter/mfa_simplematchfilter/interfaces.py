from zope import schema
from zope.interface import Interface

from mfa_core_filter.interfaces import MailSources, SimpleFilterOperators

# XXX - should inherit from IFilter
class ISimpleMatchFilter(Interface):
    """ Interface for simple match filter """
    source = schema.Choice(title=u'source',
                           source = MailSources(),
                           required=True)
    operator = schema.Choice(title=u'operator',
                             source = SimpleFilterOperators(),
                             required=True)
    condition = schema.TextLine(title=u'condition',required=True)