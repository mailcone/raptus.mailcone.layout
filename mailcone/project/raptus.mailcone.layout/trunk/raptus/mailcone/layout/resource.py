import grok

from zope.interface import Interface

from fanstatic import Library, Resource

from js.jquery import jquery
from js.jqueryui import jqueryui, smoothness
from js.jquery_datatables import jquery_datatables
from js.jquery_elastic import elastic
from js.jquery_splitter import splitter

from raptus.mailcone.layout import interfaces




library = Library('raptus.mailcone.layout', 'static')

deco = Resource(library, 'deco.css', depends=[])
reset = Resource(library, 'reset.css', depends=[])
layout = Resource(library, 'layout.css', depends=[])
jqueryuicss = Resource(library, 'jqueryui.css', depends=[])
style = Resource(library, 'style.css', depends=[])
base = Resource(library, 'base.css', depends=[smoothness, layout, deco, reset, jqueryuicss, style])



ui_elements = Resource(library, 'ui_elements.js', depends=[jquery, jqueryui, jquery_datatables, elastic, splitter])




@grok.adapter(Interface, name='raptus.mailcone.layout.ui_elements')
@grok.implementer(interfaces.IResourceProvider)
def ui_elements_resource_provider(context):
    return [ui_elements,]

@grok.adapter(Interface, name='raptus.mailcone.layout.base')
@grok.implementer(interfaces.IResourceProvider)
def style_resource_provider(context):
    return [base,]
