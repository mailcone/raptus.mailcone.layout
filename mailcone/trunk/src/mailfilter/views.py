import grok

from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter

# catalog stuff
from hurry.query.interfaces import IQuery
from hurry.query import set, Eq, And

from mailfilter.app import MailfilterApp
from mailfilter.viewletmanagers import HeadSlot, LeftColumn, Main, Footer
from mailfilter.resource import library as MailfilterLibrary
from mailfilter.resource import controlPanelCss, controlPanelJs, dashBoardJs
from mailfilter.contents import RuleSet, Rule

from mfa_core_filter.utils import IFilterManager
from mfa_core_action.utils import IActionManager

from mailfilter.interfaces import (
    IRuleJSExtenerManager,
    IControlPanel, 
    IRuleSet, 
    IRule, 
    IRuleContainer,
    ISettingConfigletManager,
    IFilterSettingConfiglet,
    IActionSettingConfiglet,
    ISmtpServerUtil
)

from mfa_core_action.interfaces import IActionManager
from mfa_core_filter.interfaces import IFilterManager

#
# Base viewlets
#
class Head(grok.Viewlet):
    """ Povide a viewlet contains base css and js stuff used by every side """
    grok.viewletmanager(HeadSlot)
    grok.context(Interface)

class NavigationViewlet(grok.Viewlet):
    """ Povide a viewlet contains main navigation """
    grok.viewletmanager(LeftColumn)
    grok.context(Interface)

class DashBoardView(grok.View):
    """ Povide front page view """
    grok.context(MailfilterApp)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')
    
    customers = None

    def _getCustomers(self):
        """ return a list of all existing customer instances """
        query = getUtility(IQuery)
        return query.searchResults(Eq(('catalog', 'content_type'), 'Customer'))

    def update(self):
        """ XXX """
        self.customers = self._getCustomers()

class DashBoardViewlet(grok.Viewlet):
    """ Povide a viewlet contains front page """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('dashboard_viewlet')
    grok.view(DashBoardView)

    def update(self):
        dashBoardJs.need()

#
# Control panel viewlets
#
class ControlPanelView(grok.View):
    """ Provide a base view for registered configlets """
    grok.context(MailfilterApp)
    grok.name('control_panel')
    grok.template('master')
    grok.require('mailfilter.view')

class ControlPanelViewlet(grok.Viewlet):
    """ Viewlet provide control panel """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('controlpanel_viewlet')
    grok.view(ControlPanelView)

    def listConfiglets(self):
        Cp = getUtility(IControlPanel)
        return Cp.listConfiglets()

    def update(self):
        """ XXX """
        controlPanelCss.need()
        controlPanelJs.need()
        # register js scripts needed for ajax
        jsExManager = getUtility(IRuleJSExtenerManager)
        for jsExtension in jsExManager.listJSExtensions():
            jsExtension.need()
            
#
# Configlets
#
class RuleSetConfigletView(grok.View):
    """ Provide view for rule set management """
    grok.context(MailfilterApp)
    grok.name('rulesetConfiglet')
    grok.template('master')
    grok.require('mailfilter.view')

    rulesets = None

    def _getRuleSets(self):
        """ return a list of all existing rule set instances """
        query = getUtility(IQuery)
        return query.searchResults(Eq(('catalog', 'content_type'), 'RuleSet'))
    
    def update(self):
        """ XXX """
        self.rulesets = self._getRuleSets()
        
        if self.request.method == 'POST':
            if self.request.get('selectRulesetButton'):
                for ruleset in self.rulesets:
                    if self.request.get('selectRuleset') == self.url(ruleset):
                        self.redirect(self.url(ruleset))  

class RuleSetConfigletViewlet(grok.Viewlet):
    """ Provide viewlet with main view for rule set configlet """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('rulesets_configlet')
    grok.view(RuleSetConfigletView)

# XXX - should be renamed to settings configlet
class AppConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(MailfilterApp)
    grok.name('appConfiglet')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

# XXX - should be renamed to settings configlet
class AppConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppConfigletView """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('app_configlet')
    grok.view(AppConfigletView)

    def listSettingConfiglets(self):
        scm = getUtility(ISettingConfigletManager)
        return scm.listConfiglets()

#
# Setting Configlets
#
class AppSettingConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(MailfilterApp)
    grok.name('appSettings')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

class AppSettingConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppSettingConfigletView """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.view(AppSettingConfigletView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editappsettings')
        self.form.update_form()

    def render(self):
        return self.form.render()

class DatabaseSettingConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(MailfilterApp)
    grok.name('databaseSettings')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

class DatabaseSettingConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppSettingConfigletView """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.view(DatabaseSettingConfigletView)
    grok.template('db_settings')
    
class SmtpSettingConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(ISmtpServerUtil)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

class SmtpSettingConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppSettingConfigletView """
    grok.viewletmanager(Main)
    grok.context(ISmtpServerUtil)
    grok.view(SmtpSettingConfigletView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editsmtpsettings')
        self.form.update_form()

    def render(self):
        return self.form.render()

#XXX - move to mfa_core_filter
class FilterSettingConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(IFilterSettingConfiglet)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

    def listSettings(self):
        fsm = getUtility(IFilterManager)
        return fsm.listFilterSettings()

#XXX - move to mfa_core_filter
class FilterSettingConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppSettingConfigletView """
    grok.viewletmanager(Main)
    grok.context(IFilterSettingConfiglet)
    grok.view(FilterSettingConfigletView)
    grok.template('object_settings_configlet')

#XXX - move to mfa_core_action
class ActionSettingConfigletView(grok.View):
    """ Provide configlet for app settings """
    grok.context(IActionSettingConfiglet)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

    def listSettings(self):
        asm = getUtility(IActionManager)
        return asm.listActionSettings()

#XXX - move to mfa_core_action
class ActionSettingConfigletViewlet(grok.Viewlet):
    """ Provide viewlet for AppSettingConfigletView """
    grok.viewletmanager(Main)
    grok.context(IActionSettingConfiglet)
    grok.view(ActionSettingConfigletView)
    grok.template('object_settings_configlet')

#
# Ruleset specific viewlets
#
class RuleSetView(grok.View):
    """ Provide main view for a rule set instance """
    grok.context(IRuleSet)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')

# XXX - should be not needed any more
#    def getEditUrl(self):
#        """ return url to edit form """
#        return self.url('edit')

    def getAddRuleUrl(self):
        """ return url to add form for a new rule """
        return self.url('addRule')

class RuleSetViewlet(grok.Viewlet):
    """ Provide viewlet with main view for rule set instances """
    grok.viewletmanager(Main)
    grok.context(IRuleSet)
    grok.template('ruleset_viewlet')
    grok.view(RuleSetView)

class AddRuleSetView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(MailfilterApp)
    grok.template('master')
    grok.name('addRuleSet')
    grok.require('mailfilter.view')

    def getActionButtonId(self):
        return 'addRuleSetButton'
    
    def getAction(self):
        return 'add'

    def update(self):
        if self.request.method == "POST":
            name = self.request.get('name')
            description = self.request.get('description')
            
            obj = RuleSet(name, description)
            self.context[obj.id] = obj
            self.redirect(self.url(obj))

class AddRuleSetViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddRuleSetForm """
    grok.viewletmanager(Main)
    grok.context(MailfilterApp)
    grok.template('ruleset_form')
    grok.view(AddRuleSetView)    

class EditRuleSetView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(IRuleSet)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')

    def getActionButtonId(self):
        return 'editRuleSetButton'
    
    def getAction(self):
        return 'save'

    def update(self):
        if self.request.method == "POST":
            self.context.name = self.request.get('name')
            self.context.description = self.request.get('description')
            self.redirect(self.url(self.context))

class EditRuleSetViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditRuleSetForm """
    grok.viewletmanager(Main)
    grok.context(IRuleSet)
    grok.template('ruleset_form')
    grok.view(EditRuleSetView)
    
class DeleteRuleSetView(grok.View):
    """ Provide delete view for rule sets - XXX maybe also as an action (like plone?) """
    grok.context(IRuleSet)
    grok.name('delete')
    grok.require('mailfilter.view')

    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delRuleset(self.context.__name__)
    
    def render(self):
        self.redirect(self.url(self.parent, 'rulesetConfiglet'))

#
# Rule specific viewlets
#
class RuleMacro(grok.View):
    """ Provide main view for a rule instance """
    grok.context(IRule)
    grok.name('macro')
    grok.template('rule_macros')
    grok.require('mailfilter.view')

class RuleView(grok.View):
    """ Provide main view for a rule instance """
    grok.context(IRule)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')

# XXX - should be not needed any more  
#    def getEditUrl(self):
#        """ return url to edit form """
#        return self.url('edit')
    
    def listFilterTypes(self):
        """ return list of filter types provided by filter manager """
        fM = getUtility(IFilterManager)
        return fM.listFilterTypes(self)

    def listActionTypes(self):
        """ return list of filter types provided by filter manager """
        aM = getUtility(IActionManager)
        return aM.listActionTypes(self)
    
    def update(self):
        if self.request.method == 'POST':
            if self.request.get('addFilter'):
                self.redirect(self.request.get('filterType'))
            if self.request.get('addAction'):
                self.redirect(self.request.get('actionType'))

class RuleViewlet(grok.Viewlet):
    """ Provide viewlet with main view for rule instances """
    grok.viewletmanager(Main)
    grok.context(IRule)
    grok.template('rule_viewlet')
    grok.view(RuleView)
    
class AddRuleView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(IRuleContainer)
    grok.template('master')
    grok.name('addRule')
    grok.require('mailfilter.view')

class AddRuleViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddRuleForm """
    grok.viewletmanager(Main)
    grok.context(IRuleContainer)
    grok.view(AddRuleView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='addruleform')
        self.form.update_form()

    def render(self):
        return self.form.render()

class EditRuleView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(IRule)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')

class EditRuleViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditRuleForm """
    grok.viewletmanager(Main)
    grok.context(IRule)
    grok.view(EditRuleView)
    
    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editruleform')
        self.form.update_form()

    def render(self):
        return self.form.render()

class DeleteRuleView(grok.View):
    """ Provide delete view for rules - XXX maybe also as an action (like plone?) """
    grok.context(IRule)
    grok.name('delete')
    grok.require('mailfilter.view')
    
    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delRule(self.context)
    
    def render(self):
        self.redirect(self.url(self.parent))

class EditIconsMacro(grok.View):
    """ Provide edit icons for item """
    grok.context(Interface)
    grok.name('editicons')
    grok.template('editicons_macro')
    grok.require('mailfilter.view')


from megrok import rdb
from mailfilter.interfaces import IFilterMailsUtility
from mailfilter.contents import Mail
class FilteringView(grok.View):
    """ XXX - maybe only for development """
    grok.context(Interface)
    grok.name('filtering')
    grok.template('master')
    grok.require('mailfilter.manageUsers')

    def filter(self): #XXX - will be done later in update function with button
        filterUtil = getUtility(IFilterMailsUtility)
        filterUtil.filterMails()

class FilteringViewlet(grok.Viewlet):
    """ XXX - maybe only for development """
    grok.context(Interface)
    grok.viewletmanager(Main)
    grok.template('filtering_view')
    grok.view(FilteringView)