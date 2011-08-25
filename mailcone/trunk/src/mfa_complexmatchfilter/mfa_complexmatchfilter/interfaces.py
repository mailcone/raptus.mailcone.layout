import re

from zope import schema
from zope.interface import Interface

from mfa_core_filter.interfaces import MailSources

# XXX - should inherit from IFilter
class IComplexMatchFilter(Interface):
    """ Interface for complex match filter """
    # XXX - must be solved in a other way - utility or anything else
    # XXX - values are not complete compare with sql columns
    source = schema.Choice(title=u'source',
                           source = MailSources(),
                           required=True)
    condition = schema.TextLine(title=u'condition',
                                required=True,
                                # XXX - must be maybe extended with other character
                                constraint=re.compile("[a-zA-Z0-9 .@$*+-]").match)