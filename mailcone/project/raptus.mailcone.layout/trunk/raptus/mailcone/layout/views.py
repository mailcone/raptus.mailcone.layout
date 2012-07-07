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

    columns = 30
    step = 4

    def render(self):
        import pdb;pdb.set_trace()
        session = rdb.Session()
        newest = session.query(Mail).order_by(desc(Mail.date)).first()
        if newest is None:
            return json.dumps([[[]]])
        result = list()
        last = newest.date
        for i in range(self.columns):
            dat = newest.date - datetime.timedelta(hours=i * self.step)
            count = session.query(Mail).filter(Mail.date, between(dat, last)).count()
            last = dat
            result.append([dat, count])
        
        return json.dumps([[result]])
        
        return """
[[
  ["06/15/2009 16:00:00", 136.01, 139.5, 134.53, 139.48],
  ["06/08/2009 16:00:00", 143.82, 144.56, 136.04, 136.97],
  ["06/01/2009 16:00:00", 136.47, 146.4, 136, 144.67],
  ["05/26/2009 16:00:00", 124.76, 135.9, 124.55, 135.81],
  ["05/18/2009 16:00:00", 123.73, 129.31, 121.57, 122.5],
  ["05/11/2009 16:00:00", 127.37, 130.96, 119.38, 122.42],
  ["05/04/2009 16:00:00", 128.24, 133.5, 126.26, 129.19],
  ["04/27/2009 16:00:00", 122.9, 127.95, 122.66, 127.24],
  ["04/20/2009 16:00:00", 121.73, 127.2, 118.6, 123.9],
  ["04/13/2009 16:00:00", 120.01, 124.25, 115.76, 123.42],
  ["04/06/2009 16:00:00", 114.94, 120, 113.28, 119.57],
  ["03/30/2009 16:00:00", 104.51, 116.13, 102.61, 115.99],
  ["03/23/2009 16:00:00", 102.71, 109.98, 101.75, 106.85],
  ["03/16/2009 16:00:00", 96.53, 103.48, 94.18, 101.59],
  ["03/09/2009 16:00:00", 84.18, 97.2, 82.57, 95.93],
  ["03/02/2009 16:00:00", 88.12, 92.77, 82.33, 85.3],
  ["02/23/2009 16:00:00", 91.65, 92.92, 86.51, 89.31],
  ["02/17/2009 16:00:00", 96.87, 97.04, 89, 91.2],
  ["02/09/2009 16:00:00", 100, 103, 95.77, 99.16],
  ["02/02/2009 16:00:00", 89.1, 100, 88.9, 99.72],
  ["01/26/2009 16:00:00", 88.86, 95, 88.3, 90.13],
  ["01/20/2009 16:00:00", 81.93, 90, 78.2, 88.36],
  ["01/12/2009 16:00:00", 90.46, 90.99, 80.05, 82.33],
  ["01/05/2009 16:00:00", 93.17, 97.17, 90.04, 90.58],
  ["12/29/2008 16:00:00", 86.52, 91.04, 84.72, 90.75],
  ["12/22/2008 16:00:00", 90.02, 90.03, 84.55, 85.81],
  ["12/15/2008 16:00:00", 95.99, 96.48, 88.02, 90],
  ["12/08/2008 16:00:00", 97.28, 103.6, 92.53, 98.27],
  ["12/01/2008 16:00:00", 91.3, 96.23, 86.5, 94],
  ["11/24/2008 16:00:00", 85.21, 95.25, 84.84, 92.67],
  ["11/17/2008 16:00:00", 88.48, 91.58, 79.14, 82.58],    
  ["11/10/2008 16:00:00", 100.17, 100.4, 86.02, 90.24],
  ["11/03/2008 16:00:00", 105.93, 111.79, 95.72, 98.24],
  ["10/27/2008 16:00:00", 95.07, 112.19, 91.86, 107.59],
  ["10/20/2008 16:00:00", 99.78, 101.25, 90.11, 96.38],
  ["10/13/2008 16:00:00", 104.55, 116.4, 85.89, 97.4],
  ["10/06/2008 16:00:00", 91.96, 101.5, 85, 96.8],
  ["09/29/2008 16:00:00", 119.62, 119.68, 94.65, 97.07],
  ["09/22/2008 16:00:00", 139.94, 140.25, 123, 128.24],
  ["09/15/2008 16:00:00", 142.03, 147.69, 120.68, 1400.91]
]]
"""


class ExceptionPage(layout.ExceptionPage):
    grok.name('index.html')



class NotFoundPage(layout.NotFoundPage):
    grok.name('index.html')



class UnauthorizedPage(layout.UnauthorizedPage):
    grok.name('index.html')










