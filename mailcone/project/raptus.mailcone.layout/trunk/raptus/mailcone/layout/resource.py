import grok

from zope.interface import Interface

from fanstatic import Library, Resource

from js.jquery import jquery
from js.jqueryui import jqueryui, smoothness
from js.jquery_datatables import jquery_datatables
from js.jquery_datatables import library as jquery_datatables_library

from js.jquery_elastic import elastic
from js.jquery_splitter import fixed_splitter
from js.jquery_cookie import cookie
from js.jquery_jqtransform import jqtransform_js
from js.jquery_caret import caret
from js.jquery_ba_resize import ba_resize_js

from horae.js.jqplot import resource as jqplot

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
    library, 'dataTables.scroller.min.js',
    depends=[jquery_datatables],
)


jquery_datatables_resize = Resource(
    library, 'dataTables.ColReorderWithResize.js',
    depends=[jquery_datatables],
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


ui_elements = Resource(library, 'ui_elements.js', depends=[jquery,
                                                           jqueryui,
                                                           jquery_datatables,
                                                           jquery_datatables_scroller,
                                                           jquery_datatables_tools,
                                                           jquery_datatables_clipboard,
                                                           jquery_datatables_resize,
                                                           elastic,
                                                           fixed_splitter,
                                                           jqtransform_js,
                                                           datetime,
                                                           cookie,
                                                           caret,
                                                           ba_resize_js,
                                                           jqplot.dateAxisRenderer,
                                                           jqplot.canvasAxisTickRenderer,
                                                           jqplot.canvasTextRenderer,
                                                           jqplot.ohlcRenderer,
                                                           jqplot.json2])




@grok.adapter(Interface, name='raptus.mailcone.layout.ui_elements')
@grok.implementer(interfaces.IResourceProvider)
def ui_elements_resource_provider(context):
    return [ui_elements,]

@grok.adapter(Interface, name='raptus.mailcone.layout.base')
@grok.implementer(interfaces.IResourceProvider)
def style_resource_provider(context):
    return [base,]