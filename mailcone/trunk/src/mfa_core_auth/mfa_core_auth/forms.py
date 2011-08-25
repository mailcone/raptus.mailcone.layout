import grok

from zope.interface import Interface
from zope.component import getUtility
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from mfa_core_auth.interfaces import IAddUserForm, IAccount, ILoginForm
from mfa_core_auth.contents import Account, UserFolder

class Login(grok.Form):
    """ Provide login from for application """
    grok.context(Interface)
    grok.require('zope.Public')
    label = "Login"
    template = grok.PageTemplateFile('custom_edit_form.pt')

    prefix = ''
    form_fields = grok.Fields(ILoginForm)

    def setUpWidgets(self, ignore_request=False):
        """XXX"""
        super(Login,self).setUpWidgets(ignore_request)
        self.widgets['camefrom'].type = 'hidden'
        
    @grok.action('login')
    def handle_login(self, **data):
        """XXX"""
        self.redirect(self.request.form.get('camefrom', self.url(grok.getSite())))

class AddUser(grok.Form):
    """ Provide form to add new user """
    grok.context(UserFolder)
    grok.name('addUser')
    grok.require('mailfilter.manageUsers')
    label = "Add user"
    template = grok.PageTemplateFile('custom_edit_form.pt')

    form_fields = grok.Fields(IAddUserForm)

    @grok.action('add')
    def handle_add(self, **data):
        """XXX"""
        users = getUtility(IAuthenticatorPlugin,'users')
        users.addUser(data['login'],data['password'],data['real_name'],data['role'])
        self.redirect(self.url(grok.getSite(),'userConfiglet'))

class EditUser(grok.EditForm):
    """ Provide form to edit user """
    grok.context(Account)
    grok.name('edit')
    grok.require('mailfilter.manageUsers')
    label = "Edit user"
    template = grok.PageTemplateFile('custom_edit_form.pt')

    form_fields = grok.Fields(IAccount)
    
    #XXX not realy a good solution, must be done better
    @grok.action('save')
    def save(self, **data):
        """ Provide save action for generate edit form """
        # XXX if new name id should be also changed
        self.applyData(self.context, **data) #XXX - should be done like handle_add in AddUser
        self.redirect(self.url(self.context.__parent__))