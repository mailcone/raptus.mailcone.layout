from fanstatic import Library, Resource
from js.jquery import jquery
from js.jqueryui import jqueryui

library = Library('mailfilter', 'static')

style = Resource(library, 'style.css')
controlPanelCss = Resource(library, 'controlpanel.css')
controlPanelJs = Resource(library, 'controlpanel.js', depends=[jquery, jqueryui])
dashBoardJs = Resource(library, 'dashboard.js', depends=[jquery, jqueryui])

rulesetJsExtender = Resource(library, 'ruleset_jsextender.js', depends=[jquery]) 