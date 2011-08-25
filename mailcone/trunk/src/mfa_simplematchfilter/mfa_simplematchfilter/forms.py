import grok

from mfa_core_filter.interfaces import IFilterContainer
from mfa_simplematchfilter.interfaces import ISimpleMatchFilter
from mfa_simplematchfilter.contents import SimpleMatchFilter

class AddSimpleMatchFilterForm(grok.AddForm):
    """ Generate add from for python code filter content - based on grok.AddFrom """
    grok.context(IFilterContainer)
    form_fields = grok.AutoFields(ISimpleMatchFilter)
    template = grok.PageTemplateFile('simplematchfilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add simple match filter"
    
    @grok.action('add', name='addSimpleMatchFilter')
    def add(self, **data):
        """ Provide action for generate form - save form data in a new simple match filter object """
        data['id'] = self.context.getNextId()
        obj = SimpleMatchFilter(**data)
        self.context.addFilter(obj)
        return self.redirect(self.url(obj))
        
class EditSimpleMatchFilterForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(ISimpleMatchFilter)
    form_fields = grok.AutoFields(ISimpleMatchFilter)
    template = grok.PageTemplateFile('simplematchfilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit simple match filter"
    
    @grok.action('save', name='editSimpleMatchFilter')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)
        return self.redirect(self.url(self.context))