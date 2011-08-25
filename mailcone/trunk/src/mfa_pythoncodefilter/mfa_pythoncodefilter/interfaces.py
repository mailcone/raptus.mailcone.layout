from zope import schema
from zope.interface import Interface

# XXX - should inherit from IFilter
class IPythonCodeFilter(Interface):
    """ Interface for python code filter """
    code = schema.SourceText(title=u'python code',
                             #XXX - think it gives a better solution, than structure description 
                             #      in pythoncodefilter_form.pt 
                             #XXX - must not be mails, must be varibales of mail self
                             description=u'<b>available variables</b><br/> \
                                           <ul> \
                                              <li>mails: <i>list of not matched mails</i></li> \
                                           </ul> <br/>\
                                           <b>use available variables:</b><br/> \
                                           ${mails}',
                             required=True)