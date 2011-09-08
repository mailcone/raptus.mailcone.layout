import os
import grok

from zope.component import getUtility

from grokcore.view.interfaces import ITemplateFileFactory


grok.templatedir('templates')


class BaseDataTable(grok.View):
    """ This class provide a base for the js.jquery_datatables.
        Two parts of view are supported by this view:
            1. the html output for included by a custom template
            2. a view for loading all data over ajax
    """
    
    grok.baseclass()
    
    
    def render(self):
        return 'json'
        
    def html(self):
        template = os.path.join(os.path.dirname(__file__),'templates','datatable.cpt')
        return getUtility(ITemplateFileFactory, name='cpt')(filename=template).render(self)