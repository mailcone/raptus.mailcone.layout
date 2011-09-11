import os
import grok
from grokcore import layout
from grokcore import message
from grokcore.view import PageTemplateFile

from zope.interface import Interface
from zope.component import getAdapters
from zope.component import getUtility

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces
from raptus.mailcone.core.interfaces import ITextIdManager

grok.templatedir('templates')


class Layout(layout.Layout):
    grok.name('layout')
    grok.context(Interface)

    def update(self):
        providers = getAdapters((self,), interfaces.IResourceProvider)
        for name, provider in providers:
            for resource in provider:
                resource.need()


class Page(layout.Page):
    """ this class do nothing yet!
        for some future project
    """
    
    grok.baseclass()


class AddForm(grok.AddForm):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))

    def add(self, obj):
        self.context[obj.id] = obj

    def create(self, data):
        raise NotImplementedError(u'concrete classes must implement create()')
    
    def name_for_id(self, obj, **data):
        return data.get('name')
    
    def apply(self, obj, **data):
        id = getUtility(ITextIdManager).idFromName(self.context, self.request, self.name_for_id(obj, **data) )
        self.context[id] = obj
        
    @grok.action(_(u'Add'), name='add')
    def handle_add(self, **data):
        obj = self.create(**data)
        self.add(obj)
        self.apply(obj, **data)
        message.send(_(u'${object} successfully added', mapping={'object': self.__name__}), u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), name='cancel', validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        """ we use only the button, the rest we do it with javascript
        """


class EditForm(grok.EditForm):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))


class DeleteForm( grok.Form):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates', 'delete_form.pt'))
    grok.implements(interfaces.IDeleteForm)
    
    @property
    def label(self):
        return _(u'Delete ${type}', mapping={'type': self.object_type()})
    
    def object_type(self):
        return _(u'Item')
    
    def item_title(self):
        raise NotImplementedError(u'concrete classes must implement item_title()')
    
    def next_url(self):
        parent = self.context.__parent__
        while queryMultiAdapter((parent, self.request), name=u'index') is None:
            parent = parent.__parent__
        return self.url(parent)
    
    def cancel_url(self):
        return self.url(self.context)
    
    def delete(self):
        del self.context.__parent__[self.context.__name__]
    
    @grok.action(_(u'Delete'))
    def handle_delete(self, **data):
        self.redirect(self.next_url())
        msg = _(u'${object} successfully deleted', mapping={'object': self.item_title()})
        self.delete()
        message.send(msg, u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        self.redirect(self.cancel_url())
        return ''


class Index(Page):
    grok.context(Interface)


class ExceptionPage(layout.ExceptionPage):
    grok.name('index.html')


import zope
class NotFoundPage(layout.NotFoundPage):
    grok.name('index.html')


class UnauthorizedPage(layout.UnauthorizedPage):
    grok.name('index.html')










