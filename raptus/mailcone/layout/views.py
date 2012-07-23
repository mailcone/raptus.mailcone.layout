import os
import grok
import json
import datetime

from megrok import rdb

from grokcore import layout
from grokcore import message
from grokcore.view import PageTemplateFile
from grokcore.layout.components import LayoutAwareFormPage

from zope import component
from zope.interface import Interface

from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.expression import between

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces
from raptus.mailcone.mails.contents import Mail
from raptus.mailcone.core.interfaces import ITextIdManager
from raptus.mailcone.core.interfaces import IMailcone

grok.templatedir('templates')

MIN_FOR_TWO_COLUMNS = 10





class Layout(layout.Layout):
    grok.name('layout')
    grok.context(Interface)

    def update(self):
        providers = component.getAdapters((self,), interfaces.IResourceProvider)
        for name, provider in providers:
            for resource in provider:
                resource.need()



class Page(layout.Page):
    """ this class do nothing yet!
        for some future project
    """
    
    grok.baseclass()



class MixingFieldSets(object):
    
    def fieldsets(self):
        widgets = [i for i in self.widgets]
        if len(widgets) < MIN_FOR_TWO_COLUMNS:
            return [widgets]
        else:
            middle = len(widgets) / 2
            left = [widget for i, widget in enumerate(widgets) if i < middle]
            right = [widget for i, widget in enumerate(widgets) if i >= middle]
            return [left, right]



class FormPage(LayoutAwareFormPage, MixingFieldSets, grok.Form, Page):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))
    grok.implements(interfaces.IForm)



class AddForm(grok.AddForm, MixingFieldSets):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))
    grok.implements(interfaces.IAddForm)
    
    def message(self, mapping=None):
        if mapping is None:
            mapping={'object': _('object')}
        return _(u'${object} successfully added', mapping=mapping)

    def add(self, obj):
        self.context.add_object(obj, obj.name)

    def create(self, data):
        raise NotImplementedError(u'concrete classes must implement create()')
    
    def apply(self, obj, **data):
        self.applyData(obj, **data)
    
    @grok.action(_(u'Add'), name='add')
    def handle_add(self, **data):
        obj = self.create(**data)
        self.apply(obj, **data)
        self.add(obj)
        message.send(self.message(), u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), name='cancel', validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        """ we use only the button, the rest we do it with javascript
        """



class EditForm(grok.EditForm, MixingFieldSets):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates','edit_form.pt'))
    grok.implements(interfaces.IEditForm)
    
    def message(self, mapping=None):
        if mapping is None:
            mapping =  dict(object= _('object'))
        return _(u'${object} successfully edited', mapping=mapping)

    def apply(self, **data):
        self.applyData(self.context, **data)

    @grok.action(_(u'Save changes'), name= 'edit')
    def handle_save(self, **data):
        self.apply(**data)
        message.send(self.message(), u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), name='cancel', validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        """ we use only the button, the rest we do it with javascript
        """



class EditFormPage(LayoutAwareFormPage, EditForm, Page):
    grok.baseclass()



class DeleteForm(grok.Form):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates', 'delete_form.pt'))
    grok.implements(interfaces.IDeleteForm)
    
    def item_title(self):
        raise NotImplementedError(u'concrete classes must implement item_title()')
    
    def message(self, mapping=None):
        if mapping is None:
            mapping={'object': _('object')}
        return _(u'${object} successfully deleted', mapping=mapping)
    
    def delete(self):
        del self.context.__parent__[self.context.__name__]
    
    @grok.action(_(u'Delete'), name='delete')
    def handle_delete(self, **data):
        self.delete()
        message.send(self.message(), u'info', u'session')
        return ''
    
    @grok.action(_(u'Cancel'), name='cancel', validator=lambda *args, **kwargs: {})
    def handle_cancel(self, **data):
        """ we use only the button, the rest we do it with javascript
        """



class DisplayForm(grok.DisplayForm):
    grok.baseclass()
    template = PageTemplateFile(os.path.join('templates', 'display_form.pt'))
    grok.implements(interfaces.IDisplayView)



class ReStructuredMixing(object):
    grok.baseclass()
    
    def default_namespace(self):
        # read rst templates as ascii.
        # use custom template
        di = super(ReStructuredMixing, self).default_namespace()
        template = os.path.join(os.path.dirname(__file__),'templates','restructured.txt')
        di['settings_overrides'] = dict(input_encoding='ascii',
                                        template=template,)
        return di



class Index(Page):
    grok.context(IMailcone)



class IndexAjaxSource(grok.View):
    grok.context(IMailcone)

    columns = 60
    step = 2

    def render(self):
        session = rdb.Session()
        newest = session.query(Mail).order_by(desc(Mail.date)).first()
        if newest is None:
            return json.dumps([[[]]])
        result = list()
        last = newest.date
        for i in range(self.columns):
            dat = newest.date - datetime.timedelta(hours=i * self.step)
            count = session.query(Mail).filter(between(Mail.date, dat, last)).count()
            last = dat
            result.append([dat, count])
        dthandler = lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(obj, datetime.datetime) else None
        return json.dumps([result], default=dthandler)


class ExceptionPage(layout.ExceptionPage):
    grok.name('index.html')



class NotFoundPage(layout.NotFoundPage):
    grok.name('index.html')



class UnauthorizedPage(layout.UnauthorizedPage):
    grok.name('index.html')










