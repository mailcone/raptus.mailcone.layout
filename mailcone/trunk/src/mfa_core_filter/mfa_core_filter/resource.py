from fanstatic import Library, Resource
from js.jquery import jquery
from js.jqueryui import jqueryui

library = Library('mfa_core_filter', 'static')

rulesetJsExtender = Resource(library, 'filter_jsextender.js', depends=[jquery]) 