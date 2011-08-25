import grok

from mfa_core_filter.interfaces import IFilterContainer
from mfa_complexmatchfilter.interfaces import IComplexMatchFilter
from mfa_complexmatchfilter.contents import ComplexMatchFilter

class AddComplexMatchFilterForm(grok.AddForm):
    """ Generate add from for complex match filter content - based on grok.AddFrom """
    grok.context(IFilterContainer)
    form_fields = grok.AutoFields(IComplexMatchFilter)
    template = grok.PageTemplateFile('complexmatchfilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add complex match filter"
    
    @grok.action('add', name='addComplexMatchFilter')
    def add(self, **data):
        """ Provide action for generate form - save form data in a new complex match filter object """
        data['id'] = self.context.getNextId()
        obj = ComplexMatchFilter(**data)
        self.context.addFilter(obj)
        return self.redirect(self.url(obj))

class EditComplexMatchFilterForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(IComplexMatchFilter)
    form_fields = grok.AutoFields(IComplexMatchFilter)
    template = grok.PageTemplateFile('complexmatchfilter_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit complex match filter"
    
    @grok.action('save', name='editComplexMatchFilter')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)
        return self.redirect(self.url(self.context))