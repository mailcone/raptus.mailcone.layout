import grok

from zope import schema
from zope.formlib.widgets import TextAreaWidget
from zope.formlib.widget import renderElement
from zope.app.form.browser.textwidgets import FileWidget

from xml.sax.saxutils import quoteattr, escape

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
    def _toFieldValue(self, input):
        value = super(ImageWidget, self)._toFieldValue(input)
        return Image(value)