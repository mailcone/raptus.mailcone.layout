import grok
from persistent import Persistent
from z3c.blobfile.image import Image
from xml.sax.saxutils import quoteattr, escape

from zope import schema
from zope.formlib.widget import renderElement
from zope.app.form.browser import textwidgets
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
            st = st.replace('${%s}'% term.token, str(value))
        return st



class ProposeTextField(schema.Choice, schema.Text):
    grok.implements(interfaces.IProposeTextField)

    def __init__(self, *args, **kw):
        super(ProposeTextField, self).__init__(*args, **kw)
        if not 'constraint' in kw:
            self.constraint = lambda v:schema.Text.constraint(self, v)

    def validate(self, value):
        return schema.Text.validate(self, value)

    def _validate(self, value):
        return schema.Text._validate(self, value)

    def get(self, object):
        value = super(ProposeTextField, self).get(object)
        if isinstance(value, basestring):
            return ProposeTextProxy(value, self.vocabularyName)
        return value
        
    def set(self, object, value):
        super(ProposeTextField, self).set(object, ProposeTextProxy(value, self.vocabularyName))



class ProposeTextWidget(TextAreaWidget):
    
    def __init__(self, field, vocabulary, request):
        self.choice = MultiSelectWidget(field, vocabulary, request)
        self.choice.name = ''
        super(TextAreaWidget, self).__init__(field, request)
    
    def __call__(self):
        area = super(ProposeTextWidget, self).__call__()
        choice = self.choice()
        attr = {'name':self.name,
                'id':self.name,
                'cssClass': 'propose-widget' + self.cssClass,
                'contents':area + choice}
        return renderElement('div', **attr)

    def _getCurrentValueHelper(self):
        input_value = None
        if self._renderedValueSet():
            # fetch original message
            if self._data is not None:
                input_value = self._data.original
        else:
            if self.hasInput():
                # It's insane to use getInputValue this way. It can
                # cause _error to get set spuriously.  We'll work
                # around this by saving and restoring _error if
                # necessary.
                error = self._error
                try:
                    input_value = self.getInputValue()
                finally:
                    self._error = error
            else:
                input_value = self._getDefault()
        return input_value



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




