import grok

from megrok import navigation

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces

class MainNavigation(navigation.Menu):
    """ Main navigation
    """
    grok.implements(interfaces.IMainNavigation)
    grok.name('navigation.main')
    cssClass = 'nav main-nav ui-accordion uldata'
    
    _ = lambda args:args
    navigation.submenu('menu.overview', _(u'Overview'), order=10)
    navigation.submenu('menu.preferences', _(u'Preferences'), order=20)


class HeaderNavigation(navigation.Menu):
    grok.implements(interfaces.IHeaderNavigation)
    grok.name('navigation.header')
    cssClass = 'nav header-nav'

    navigation.submenu('menu.add', 'User: Samuel Riolo', order=20)
    navigation.submenu('menu.manage', 'login', order=30)



class OverviewMenu(navigation.Menu):

    grok.implements(interfaces.IOverviewMenu)
    grok.name('menu.overview')
    cssClass = 'menu menu-overview'


class PrefernecesMenu(navigation.Menu):

    grok.implements(interfaces.IPreferencesMenu)
    grok.name('menu.preferences')
    cssClass = 'menu menu-preferences'






# debug stuff
from megrok.navigation import interfaces
class IContextualManageMenu(interfaces.IMenu):pass
class IActionsMenu(interfaces.IMenu):pass
class IAddMenu(interfaces.IMenu):pass
class ContextualManageMenu(navigation.Menu):
    """ Contextual manage menu
    """
    grok.implements(IContextualManageMenu)
    grok.name('menu.manage')
    cssClass = 'menu menu-manage'

class ActionsMenu(navigation.Menu):
    """ Actions menu
    """
    
    grok.implements(IActionsMenu)
    grok.name('menu.actions')
    cssClass = 'menu menu-actions'

    _ = lambda args:args
    navigation.submenu('menu.add', _(u'Add'), order=10)
    navigation.submenu('menu.manage', _(u'Manage'), order=30)


class AddMenu(navigation.Menu):
    """ Add menu
    """
    grok.implements(IAddMenu)
    grok.name('menu.add')
    cssClass = 'menu menu-add'