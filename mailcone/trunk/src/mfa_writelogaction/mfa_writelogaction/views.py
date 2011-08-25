import grok
from zope.component import getMultiAdapter

from mfa_core_action.interfaces import IActionContainer
from mailfilter.viewletmanagers import Main
from mfa_writelogaction.interfaces import (
    IWriteLogAction, 
    IWriteLogActionSettingObject,
    ILogfile
)
from mfa_writelogaction.contents import WriteLogAction

class AddWriteLogActionView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(IActionContainer)
    grok.template('master')
    grok.name('addWriteLogAction')
    grok.require('mailfilter.view')

class AddWriteLogActionViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddWriteLogActionForm """
    grok.viewletmanager(Main)
    grok.context(IActionContainer)
    grok.view(AddWriteLogActionView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='addwritelogactionform')
        self.form.update_form()

    def render(self):
        return self.form.render()

class WriteLogActionView(grok.View):
    """ View for write log action - redirect to parent object view """
    grok.context(IWriteLogAction)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')

class WriteLogActionViewlet(grok.Viewlet):
    """ XXX """
    grok.context(IWriteLogAction)
    grok.template('writelogaction_viewlet')
    grok.viewletmanager(Main)
    grok.view(WriteLogActionView)

class WriteLogActionMacro(grok.View):
    """ Provide an html snippet for wirte log actions """
    grok.context(IWriteLogAction)
    grok.name('macro')
    grok.template('writelogaction_macro')
    grok.require('mailfilter.view')

class EditWriteLogActionView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(IWriteLogAction)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')

class EditWriteLogActionViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditWriteLogActionForm """
    grok.viewletmanager(Main)
    grok.context(IWriteLogAction)
    grok.view(EditWriteLogActionView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editwritelogactionform')
        self.form.update_form()

    def render(self):
        return self.form.render()
    
class DeleteWriteLogActionView(grok.View):
    # XXX - not the right solution make it as grok.traversable    
    grok.context(IWriteLogAction)
    grok.name('delete')
    grok.require('mailfilter.view')
    
    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delAction(self.context)
    
    def render(self):
        self.redirect(self.url(self.parent))
        
class WriteLogActionSettingView(grok.View):
    """ XXX """
    grok.context(IWriteLogActionSettingObject)
    grok.template('master')
    grok.name('index')
    grok.require('mailfilter.manageUsers')
    
    def listLogfiles(self):
        """ XXX """
        return self.context.getLogfiles()

class WriteLogActionSettingViewlet(grok.Viewlet):
    """ XXX """
    grok.context(IWriteLogActionSettingObject)
    grok.template('setting_view')
    grok.view(WriteLogActionSettingView)
    grok.viewletmanager(Main)
    
class AddLogfileView(grok.View):
    """ XXX """
    grok.context(IWriteLogActionSettingObject)
    grok.template('master')
    grok.require('mailfilter.manageUsers')
    grok.name('addLogfile')
    
class AddLogfileViewlet(grok.Viewlet):
    grok.context(IWriteLogActionSettingObject)
    grok.view(AddLogfileView)
    grok.viewletmanager(Main)
    
    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='addlogfileform')
        self.form.update_form()
        
    def render(self):
        return self.form.render()
    
class LogfileView(grok.View):
    """ XXX """
    grok.context(ILogfile)
    grok.template('master')
    grok.require('mailfilter.manageUsers')
    grok.name('index')
    
class LogfileViewlet(grok.Viewlet):
    """ XXX """
    grok.context(ILogfile)
    grok.template('logfile_viewlet')
    grok.viewletmanager(Main)
    grok.view(LogfileView)
    
class EditLogfileView(grok.View):
    """ XXX """
    grok.context(ILogfile)
    grok.template('master')
    grok.require('mailfilter.manageUsers')
    grok.name('edit')
    
class EditLogfileViewlet(grok.Viewlet):
    """ XXX """
    grok.context(ILogfile)
    grok.viewletmanager(Main)
    grok.view(EditLogfileView)
    
    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editlogfileform')
        self.form.update_form()
        
    def render(self):
        return self.form.render()
    
class LogfileMacro(grok.View):
    """ Provide macros for logfile contents """
    grok.context(ILogfile)
    grok.name('macro')
    grok.template('logfile_macro')
    grok.require('mailfilter.manageUsers')
    
class DeleteLogfile(grok.View):
    # XXX - not the right solution make it as grok.traversable    
    grok.context(ILogfile)
    grok.name('delete')
    grok.require('mailfilter.manageUsers')
    
    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delLogfile(self.context)
    
    def render(self):
        self.redirect(self.url(self.parent))