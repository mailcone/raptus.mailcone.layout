import grok

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import interface

from megrok.navigation import interfaces



class IMailconeBrowserLayer(IDefaultBrowserLayer):
    """ Mailcone browser layer
    """
    grok.skin('default')


class IResourceProvider(interface.Interface):
    """ A provider for fanstatic resources to be included in any horae.layout view
    """
    
    def __iter__():
        """ The fanstatic resources to be included
        """
        

class IMainNavigation(interfaces.IMenu):
    """ Main navigation
    """


class IHeaderNavigation(interfaces.IMenu):
    """ Header navigation
    """


class IOverviewMenu(interfaces.IMenu):
    """ submenu for mainnavigation
    """


class IPreferencesMenu(interfaces.IMenu):
    """ submenu for mainnavigation
    """



