import grok

from mfa_core_filter.interfaces import IFilterContainer
from mfa_pythoncodefilter.interfaces import IPythonCodeFilter
from mfa_pythoncodefilter.contents import PythonCodeFilter

class AddPythonCodeFilterForm(grok.AddForm):
    """ Generate add from for python code filter content - based on grok.AddFrom """
    grok.context(IFilterContainer)
    form_fields = grok.AutoFields(IPythonCodeFilter)
    template = grok.PageTemplateFile('pythoncodefilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add python code filter"
    
    @grok.action('add', name='addPythonCodeFilter')
    def add(self, **data):
        """ Provide action for generate form - save form data in a new python code filter object """
        data['id'] = self.context.getNextId()
        obj = PythonCodeFilter(**data)
        self.context.addFilter(obj)
        return self.redirect(self.url(obj))
        
class EditPythonCodeFilterForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(IPythonCodeFilter)
    form_fields = grok.AutoFields(IPythonCodeFilter)
    template = grok.PageTemplateFile('pythoncodefilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit python code filter"
    
    @grok.action('save', name='editPythonCodeFilter')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)
        return self.redirect(self.url(self.context))