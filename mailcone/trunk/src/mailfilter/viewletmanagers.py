# grok stuff
import grok
from zope.interface import Interface

class HeadSlot(grok.ViewletManager):
    """ Povide a viewlet manager for html header stuff """
    grok.context(Interface)
    grok.name('headslot')
    
class Header(grok.ViewletManager):
    """ Povide a viewlet manager for header viewlets """
    grok.context(Interface)
    grok.name('header')

class LeftColumn(grok.ViewletManager):
    """ Povide a viewlet manager for viewlets in a column left of main content """
    grok.context(Interface)
    grok.name('leftcolumn')
    
class RightColumn(grok.ViewletManager):
    """ Povide a viewlet manager for viewlets in a column right of main content
        not in use at the moment """
    grok.context(Interface)
    grok.name('rightcolumn')
    
class Main(grok.ViewletManager):
    """ Povide a viewlet manager for viewlets for the main content """
    grok.context(Interface)
    grok.name('main')
    
class Footer(grok.ViewletManager):
    """ Povide a viewlet manager for viewlets for footer viewlets """
    grok.context(Interface)
    grok.name('footer')