import grok
import martian

from zope.component import queryUtility

from megrok import navigation
from megrok.navigation.interfaces import IMenu

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces
from raptus.mailcone.core.interfaces import IContainerLocator


class MainNavigation(navigation.Menu):
    """ Main navigation
    """
    grok.implements(interfaces.IMainNavigation)
    grok.name('navigation.main')
    cssClass = 'nav main-nav ui-accordion uldata'
    
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





class locatormenuitem(navigation.menuitem):
    """ directive for creating a action
        to locate a instance
        implementing raptus.mailcone.core.interfaces.IContainerLocator
    """
    
    store = martian.ONCE

    def factory(self, menu, locator, title=None, order=0, icon=None, group=''):
        martian.validateInterfaceOrClass(self, menu)
        martian.validateInterfaceOrClass(self, locator)
        if not (issubclass(locator, IContainerLocator) or ILocatorContainer.implementedBy(locator)):
            raise martian.error.GrokImportError(
                "You can only pass a class implementing "
                "raptus.mailcone.core.interfaces.IContainerLocator "
                "to the '%s' directive." % self.name)
        if not (issubclass(menu, IMenu) or IMenu.implementedBy(menu)):
            raise martian.error.GrokImportError(
                "You can only pass a class implementing "
                "megrok.navigation.interfaces.IMenu "
                "to the '%s' directive." % self.name)
        return menu, (locator, title, order, icon, group)


class LocatorMenuItem(navigation.MenuItem):
    grok.baseclass()

    @property
    def link(self):
        locator = queryUtility(self.locator)
        if locator is None:
            return None
        return '%s/%s' % (locator.url(self.request), self.viewName)


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