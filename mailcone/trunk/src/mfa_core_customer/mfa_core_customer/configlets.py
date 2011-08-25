# grok stuff
import grok

from mailfilter.interfaces import IConfiglet

class CustomerConfiglet (grok.GlobalUtility):
    """ Utility provide a gui to manage customers """
    grok.implements(IConfiglet)
    grok.name('CustomerConfiglet')

    id = 'CustomerConfiglet' # defines link id
    title = 'customers' # defines link content
    url = 'customerConfiglet'