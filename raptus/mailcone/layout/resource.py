import grok

from zope.interface import Interface

from fanstatic import Library, Resource

from js.jquery import jquery
from js.jqueryui import jqueryui, smoothness
from js.jquery_datatables import jquery_datatables
from js.jquery_datatables import library as jquery_datatables_library

from js.jquery_elastic import elastic
from js.jquery_splitter import splitter
from js.jquery_jqtransform import jqtransform_js

from horae.datetime.resource import spinbox as datetime
from horae.datetime.resource import css as spinbox_css



from raptus.mailcone.layout import interfaces




library = Library('raptus.mailcone.layout', 'static')

deco = Resource(library, 'deco.css', depends=[])
reset = Resource(library, 'reset.css', depends=[])
layout = Resource(library, 'layout.css', depends=[])
forms = Resource(library, 'forms.css', depends=[])
jqueryuicss = Resource(library, 'jqueryui.css', depends=[])
style = Resource(library, 'style.css', depends=[])
base = Resource(library, 'base.css', depends=[smoothness, layout, deco, reset, jqueryuicss, style, forms, spinbox_css])





jquery_datatables_scroller = Resource(
    jquery_datatables_library, 'extras/Scroller/media/js/Scroller.js',
    depends=[jquery_datatables],
    minified='extras/Scroller/media/js/Scroller.min.js'
)

jquery_datatables_tools = Resource(
    jquery_datatables_library, 'extras/TableTools/media/js/TableTools.js',
    depends=[jquery_datatables],
    minified='extras/TableTools/media/js/TableTools.min.js'
)

jquery_datatables_clipboard = Resource(
    jquery_datatables_library, 'extras/TableTools/media/js/ZeroClipboard.js',
    depends=[jquery_datatables],
)


jquery_cookie = Resource(library, 'jquery.cookie.js', depends=[jquery])

@grok.adapter(Interface, name='raptus.mailcone.layout.jquery.cookie')
@grok.implementer(interfaces.IResourceProvider)
def jquery_cookie_resource_provider(context):
    return [jquery_cookie,]


ui_elements = Resource(library, 'ui_elements.js', depends=[jquery,
                                                           jqueryui,
                                                           jquery_datatables,
                                                           jquery_datatables_scroller,
                                                           jquery_datatables_tools,
                                                           jquery_datatables_clipboard,
                                                           elastic,
                                                           splitter,
                                                           jqtransform_js,
                                                           datetime,
                                                           jquery_cookie])




@grok.adapter(Interface, name='raptus.mailcone.layout.ui_elements')
@grok.implementer(interfaces.IResourceProvider)
def ui_elements_resource_provider(context):
    return [ui_elements,]

@grok.adapter(Interface, name='raptus.mailcone.layout.base')
@grok.implementer(interfaces.IResourceProvider)
def style_resource_provider(context):
    return [base,]