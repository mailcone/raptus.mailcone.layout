import grok
from zope.component import getMultiAdapter

from mfa_core_filter.interfaces import IFilterContainer
from mailfilter.viewletmanagers import Main
from mfa_pythoncodefilter.interfaces import IPythonCodeFilter
from mfa_pythoncodefilter.contents import PythonCodeFilter

class AddPythonCodeFilterView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(IFilterContainer)
    grok.template('master')
    grok.name('addPythonFilter')
    grok.require('mailfilter.view')

class AddPythonCodeFilterViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddPythonCodeFilterForm """
    grok.viewletmanager(Main)
    grok.context(IFilterContainer)
    grok.view(AddPythonCodeFilterView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='addpythoncodefilterform')
        self.form.update_form()

    def render(self):
        return self.form.render()
    
class PythonCodeFilterView(grok.View):
    """ View for python code filter - redirect to parent object view """
    grok.context(IPythonCodeFilter)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')

class PythonCodeFilterViewlet(grok.Viewlet):
    """ XXX """
    grok.context(IPythonCodeFilter)
    grok.template('pythoncodefilter_viewlet')
    grok.viewletmanager(Main)
    grok.view(PythonCodeFilterView)

class PythonCodeFilterMacro(grok.View):
    """ Provide an html snippet for python code filters """
    grok.context(IPythonCodeFilter)
    grok.name('macro')
    grok.template('pythoncodefilter_macro')
    grok.require('mailfilter.view')

class EditPythonCodeFilterView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(IPythonCodeFilter)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')

class EditPythonCodeFilterViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditPythonCodeFilterForm """
    grok.viewletmanager(Main)
    grok.context(IPythonCodeFilter)
    grok.view(EditPythonCodeFilterView)
    
    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editpythoncodefilterform')
        self.form.update_form()

    def render(self):
        return self.form.render()
    
class DeletePythonCodeFilterView(grok.View):
    grok.context(IPythonCodeFilter)
    grok.name('delete')
    grok.require('mailfilter.view')
    
    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delFilter(self.context)
    
    def render(self):
        self.redirect(self.url(self.parent))