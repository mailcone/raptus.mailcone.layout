import grok
import grokcore
import martian

from zope import interface
from zope.component import queryUtility
from zope.publisher.interfaces import IRequest
from zope.pagetemplate.interfaces import IPageTemplate

from megrok import navigation
from megrok.navigation.interfaces import IMenu
from megrok.navigation.interfaces import IMenuItem

from raptus.mailcone.layout import _
from raptus.mailcone.layout import interfaces
from raptus.mailcone.core.interfaces import IContainerLocator


grok.templatedir('templates')





class ItemTemplate(grok.MultiAdapter, grok.View):
    grok.implements(IPageTemplate)
    grok.provides(IPageTemplate)
    grok.context(interface.Interface)
    grok.adapts(IMenuItem, IRequest)
    grok.template('navigation_item')

    def __call__(self):
        return self.template.render(self)

    def default_namespace(self):
        di = self.context.default_namespace()
        di['template'] = self
        return di
    
    @property
    def activestate(self):
        return str(self.request.URL).startswith(str(self.context.link))



class MainNavigationMenu(navigation.Menu):
    """ Main navigation
    """
    grok.implements(interfaces.IMainNavigation)
    grok.name('navigation.main')
    cssClass = 'nav main-nav ui-accordion uldata'
    
    navigation.submenu('menu.overview', _(u'Overview'), order=10)
    navigation.submenu('menu.preferences', _(u'Preferences'), order=20)
    navigation.submenu('menu.cronjob', _(u'Cronjob'), order=30)



class HeaderNavigationMenu(navigation.Menu):
    grok.implements(interfaces.IHeaderNavigation)
    grok.name('navigation.header')
    cssClass = 'nav header-nav'



class OverviewMenu(navigation.Menu):

    grok.implements(interfaces.IOverviewMenu)
    grok.name('menu.overview')
    cssClass = 'menu menu-overview'



class PrefernecesMenu(navigation.Menu):

    grok.implements(interfaces.IPreferencesMenu)
    grok.name('menu.preferences')
    cssClass = 'menu menu-preferences'



class CronjobMenu(navigation.Menu):

    grok.implements(interfaces.ICronjobMenu)
    grok.name('menu.cronjob')
    cssClass = 'menu menu-cronjob'



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



