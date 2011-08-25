from fanstatic import Library, Resource
from js.jquery import jquery
from js.jqueryui import jqueryui

library = Library('mfa_core_action', 'static')

rulesetJsExtender = Resource(library, 'action_jsextender.js', depends=[jquery]) 