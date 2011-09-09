import os
import grok
from grokcore import layout
from grokcore.view import PageTemplateFile

from zope.interface import Interface
from zope.component import getAdapters

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces

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
    
    def apply(self, obj, **data):
        obj(obj)
        
    @grok.action(_(u'Add'), name='add')
    def handle_add(self, **data):
        obj = self.create(**data)
        self.add(obj)
        self.apply(obj, **data)
        self.redirect(self.next_url(obj))
        message.send(_(u'${object} successfully added', mapping={'object': self.object_type()}), u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), name='cancel', validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        """ we use only the button, the rest we do it with javascript
        """


class EditForm(grok.EditForm):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))


class Index(Page):
    grok.context(Interface)


class ExceptionPage(layout.ExceptionPage):
    grok.name('index.html')


import zope
class NotFoundPage(layout.NotFoundPage):
    grok.name('index.html')


class UnauthorizedPage(layout.UnauthorizedPage):
    grok.name('index.html')










