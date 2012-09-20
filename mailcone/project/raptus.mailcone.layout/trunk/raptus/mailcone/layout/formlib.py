import grok
from persistent import Persistent
from z3c.blobfile.image import Image
from xml.sax.saxutils import quoteattr, escape

from zope import schema
from zope.formlib.widget import renderElement
from zope.app.form.browser import textwidgets
from zope.schema._bootstrapfields import ValidatedProperty
from zope.schema._bootstrapinterfaces import WrongType
from zope.app.form.browser.textwidgets import FileWidget
from zope.formlib.widgets import TextAreaWidget, MultiSelectWidget, ItemDisplayWidget

from zc.datetimewidget.datetimewidget import DatetimeDisplayBase as DatetimeDisplayBaseBase

from raptus.mailcone.layout import interfaces





class CodeField(schema.Text):
    grok.implements(interfaces.ICodeField)
    
    def __init__(self, *args, **kw):
        self.mode = kw.pop('mode')
        super(CodeField, self).__init__(*args, **kw)



class CodeWidget(TextAreaWidget):
    
    def __call__(self):
        
        attr = {'name':self.name,
                'id':self.name,
                'cssClass':'ui-codemirror %s' % self.cssClass,
                'rows':self.height,
                'cols':self.width,
                'style':self.style,
                'data-mode':self.context.mode,
                'contents':escape(self._getFormValue()),
                'extra':self.extra}
                
        return renderElement('code', **attr)



class ImageWidget(FileWidget):
    """ http://www.stereoplex.com/blog/blob-support-in-the-zodb-with-zeo
    """
    def _toFieldValue(self, input):
        value = super(ImageWidget, self)._toFieldValue(input)
        if not value:
            return None
        return Image(value)



class ProposeTextProxy(Persistent):
    
    def __init__(self, text, vocabularyName):
        self.original = text
        self.vocabularyName = vocabularyName
    
    def __repr__(self):
        return '<%s@%s "%s">' % (self.__class__.__name__, hex(id(self)), self.original)
    
    def __str__(self):
        return self.original
    
    def __eq__(self, comp):
        return comp.original is self.original

    def keys(self, context):
        registry = schema.vocabulary.getVocabularyRegistry()
        vocabulary = registry.get(context, self.vocabularyName)
        for term in vocabulary:
            yield term.token
    
    def encode(self, context, replacements):
        st = self.original
        registry = schema.vocabulary.getVocabularyRegistry()
        vocabulary = registry.get(context, self.vocabularyName)
        for term in vocabulary:
            value = replacements.get(term.token, term.value)
            st = st.replace('${%s}'% term.token, unicode(value))
        return st



def propose_text_field_check(instance, value):
    if not isinstance(value, ProposeTextProxy):
        raise WrongType('%s but ProposeTextProxy is required' % repr(value))



class ProposeTextField(schema.Choice, schema.Text):
    grok.implements(interfaces.IProposeTextField)

    default = ValidatedProperty('default', propose_text_field_check)

    def __init__(self, *args, **kw):
        self.missing_value = ProposeTextProxy('', kw.get('vocabulary', ''))
        kw['default'] = ProposeTextProxy(kw.get('default', ''), kw.get('vocabulary', ''))
        super(ProposeTextField, self).__init__(*args, **kw)
        if not 'constraint' in kw:
            self.constraint = lambda v:schema.Text.constraint(self, v)

    def _validate(self, value):
        return schema.Text._validate(self, value.original)



class ProposeTextWidget(TextAreaWidget):
    
    def __init__(self, field, vocabulary, request):
        fake_field = schema.Choice(vocabulary)
        fake_field.context = object()
        self.choice = MultiSelectWidget(fake_field, vocabulary, request)
        self.choice.name = 'dummy'
        self.choice._data = list()
        self._missing = field.default
        super(TextAreaWidget, self).__init__(field, request)
    
    def __call__(self):
        area = super(ProposeTextWidget, self).__call__()
        choice = self.choice()
        attr = {'name':self.name,
                'id':self.name,
                'cssClass': 'propose-widget' + self.cssClass,
                'contents':area + choice}
        return renderElement('div', **attr)

    def _toFieldValue(self, input):
        if input == self._missing.original:
            return self.context.missing_value
        else:
            return ProposeTextProxy(input, self.context.vocabularyName)

    def _toFormValue(self, value):
        if value == self.context.missing_value:
            value = self._missing
        return value.original

    def _getCurrentValue(self):
        return super(ProposeTextWidget, self)._getCurrentValue().original



class ProposeTextDisplayWidget(TextAreaWidget):
    
    def __init__(self, field, vocabulary, request):
        super(ProposeTextDisplayWidget, self).__init__(field, request)



class DatetimeDisplayBase(DatetimeDisplayBaseBase):
    """ remove time location at all.
    """

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        if content == self.context.missing_value:
            return ""
        #content = localizeDateTime(content, self.request)
        formatter = self.request.locale.dates.getFormatter(
            self._category, (self.displayStyle or None))
        content = formatter.format(content)
        return renderElement("span", contents=textwidgets.escape(content),
                             cssClass=self.cssClass)


class DatetimeDisplayWidget(
    DatetimeDisplayBase, textwidgets.DatetimeDisplayWidget):
    pass



class DateDisplayWidget(DatetimeDisplayBase, textwidgets.DateDisplayWidget):
    pass




