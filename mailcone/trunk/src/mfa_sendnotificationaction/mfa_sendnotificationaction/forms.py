import grok

from mfa_core_action.interfaces import IActionContainer
from mfa_sendnotificationaction.interfaces import ISendNotificationAction
from mfa_sendnotificationaction.contents import SendNotificationAction

class AddSendNotificationActionForm(grok.AddForm):
    """ Generate add from for send notification action content - based on grok.AddFrom """
    grok.context(IActionContainer)
    form_fields = grok.AutoFields(ISendNotificationAction)
    template = grok.PageTemplateFile('sendnotificationaction_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add send notification action"
    
    @grok.action('add', name='addSendNotificationAction')
    def add(self, **data):
        """ Provide action for generate form - save form data in a new send notification action object """
        data['id'] = self.context.getNextId()
        obj = SendNotificationAction(**data)
        self.context.addAction(obj)
        return self.redirect(self.url(obj))
        
class EditSendNotficiationActionForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(ISendNotificationAction)
    form_fields = grok.AutoFields(ISendNotificationAction)
    template = grok.PageTemplateFile('sendnotificationaction_form.pt')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit send notification action"
    
    @grok.action('save', name='editSendNotificationAction')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)
        return self.redirect(self.url(self.context))