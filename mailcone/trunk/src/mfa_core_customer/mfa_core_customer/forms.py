#
# at the moment not needed
#

import grok

from mailfilter.app import MailfilterApp
from mfa_core_customer.interfaces import ICustomer
from mfa_core_customer.contents import Customer

class AddCustomerForm(grok.AddForm):
    """ Generate add from for customer content - based on grok.AddFrom """
    grok.context(MailfilterApp)
    form_fields = grok.AutoFields(ICustomer).omit('id')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add a customer"
    
    @grok.action('Add customer')
    def add(self, **data):
        """ Provide add action for generate form - save form data in a new customer object """
        obj = Customer(**data)
        self.context[obj.id] = obj

class EditCustomerForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(ICustomer)
    form_fields = grok.AutoFields(ICustomer).omit('id')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit customer"
    
    @grok.action('save')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)