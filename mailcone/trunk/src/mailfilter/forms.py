import grok

from datetime import datetime

from zope.component import getUtility

from mailfilter.app import MailfilterApp
from mailfilter.interfaces import (
    IRuleSet, 
    IRuleContainer, 
    IRule, 
    IMailfilterApp,
    IDatabaseSettings,
    ISmtpServerUtil
)
from mailfilter.contents import RuleSet, Rule

#
# App configuration
#
class EditAppSettings(grok.EditForm):
    """ XXX """
    grok.context(MailfilterApp)
    form_fields = grok.AutoFields(IMailfilterApp)
    grok.require('mailfilter.manageUsers')
    label = "Edit app configurations"
    
    @grok.action('save', name='saveAppSettings')
    def save(self, **data):
        """ XXX"""
        self.applyData(self.context, **data)

class EditDbSettings(grok.EditForm):
    """ XXX """
    grok.context(MailfilterApp)
    form_fields = grok.AutoFields(IDatabaseSettings)
    grok.require('mailfilter.manageUsers')
    label = "Edit database configurations"
    
    @grok.action('save', name='saveDatabaseSettings')
    def save(self, **data):
        """ XXX"""
        self.applyData(self.context, **data)

class EditSmtpSettings(grok.EditForm):
    """ XXX """
    grok.context(ISmtpServerUtil)
    form_fields = grok.AutoFields(ISmtpServerUtil)
    grok.require('mailfilter.manageUsers')
    label = "Edit smtp server configurations"
    
    @grok.action('save', name='saveSmtpSettings')
    def save(self, **data):
        """ XXX"""
        self.applyData(self.context, **data)

# XXX - maybe in a future version
#    @grok.action('send test mail', name='sendTestMail')
#    def sendTestMail(self, **data):
#        """ save data and send a test mail with given settings """
#        self.save(**data)       
#        mail = MIMEText("This is a testmail from mailcone application.")
#        mail['To'] = data['form.to']
#        mail['Subject'] = 'Subject'
#        su = getUtility(ISmtpServerUtil)
#        su.send(mail)
        
#
# RuleSet specific forms
#
class AddRuleSetForm(grok.AddForm):
    """ Generate add from for rule set content - based on grok.AddFrom """ 
    grok.context(MailfilterApp)
    form_fields = grok.AutoFields(IRuleSet).omit('id')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add a rule set"
    
    @grok.action('Add rule set')
    def add(self, **data):
        """ Provide add action for generate form - save form data in a new rule set object """
        obj = RuleSet(**data)
        self.context[obj.id] = obj

class EditRuleSetForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(IRuleSet)
    form_fields = grok.AutoFields(IRuleSet).omit ('id')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit rule set"
    
    @grok.action('save')
    def save(self, **data):
        """ Provide save action for generate edit form """
        self.applyData(self.context, **data)
        # XXX if new name id should be also changed

#
# Rule specific forms
#
class AddRuleForm(grok.AddForm):
    """ Generate add from for rule content - based on grok.AddFrom """
    grok.context(IRuleContainer)
    form_fields = grok.AutoFields(IRule).omit ('id', 'last_modification', 'last_modi_user', 'last_match')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Add a rule"

    @grok.action('add', name='addRule')
    def add(self, **data):
        """ Provide add action for generate form - save form data in a new rule object """
        #XXX - must be done better - util which provide this, maybe allready exist
        data ['last_modi_user'] = self.request.principal
        newRule = Rule(**data)
        self.context.addRule(newRule)
        return self.redirect(self.url(newRule))

class EditRuleForm(grok.EditForm):
    """ Provides generic form for edit """
    grok.context(IRule)
    form_fields = grok.AutoFields(IRule).omit ('id', 'last_modification', 'last_modi_user', 'last_match')
    #XXX set right permission
    grok.require('mailfilter.view')
    label = "Edit rule"
    
    @grok.action('save', name='editRule')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data)
        # XXX - should be done later in a Event IObjectCreatedEvent and IContainerModifiedEvent
        self.context.setLastModificationDate(datetime.now())
        #XXX - must be done better - util which provide this, maybe allready exist
        self.context.setLastModificationUser(self.request.principal)
        return self.redirect(self.url(self.context))