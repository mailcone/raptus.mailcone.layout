import grok

from zope import schema
from zope.formlib.widgets import TextAreaWidget
from zope.formlib.widget import renderElement
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