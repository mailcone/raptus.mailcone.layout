import grok

from mfa_core_action.interfaces import IAction

class Action(object):
    """XXX"""
    grok.implements(IAction)