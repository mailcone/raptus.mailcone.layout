import grok

from megrok import navigation

from raptus.mailcone.layout import interfaces

class MainNavigation(navigation.Menu):
    """ Main navigation
    """
    grok.implements(interfaces.IMainNavigation)
    grok.name('navigation.main')
    cssClass = 'nav main-nav ui-accordion uldata'
    
    _ = lambda args:args
    navigation.submenu('menu.add', _(u'Add'), order=10)
    navigation.submenu('menu.actions', _(u'Actions'), order=20)
    navigation.submenu('menu.manage', _(u'Manage'), order=30)


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