import grok

from zope import interface
from zope.schema.interfaces import IText, IChoice
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

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


class ICronjobMenu(interfaces.IMenu):
    """ submenu for cronjobs
    """


class IAddForm(interfaces.Interface):
    """ Basic add form
    """
    def message(self, mapping=None):
        """ return a message mapping
        """

    def add(self, obj):
        """ add the object to context
        """

    def create(self, data):
        """ return a new object
        """

    def apply(self, obj, **data):
        """ fill form data to object
        """
        
        
class IEditForm(interface.Interface):
    """ Basic edit form
    """

    def message(self, mapping=None):
        """ return a message mapping
        """

    def apply(self, obj, **data):
        """ fill form data to object
        """
        

class IDeleteForm(interface.Interface):
    """ Basic delete form
    """
    
    def item_title():
        """ Returns the title of the object to be deleted
        """
    
    def next_url():
        """ Returns the url to be redirected to after successful deletion
        """
    
    def cancel_url():
        """ Returns the url to be redirected to after cancellation
        """
    
    def delete():
        """ Deletes the object
        """


class IDisplayView(interface.Interface):
    """ Marker interface for display views
    """
    

class ICodeField(IText):
    """ javascript codemirror field
    """



class IProposeTextField(IChoice):
    """ textarea with vocabulary as proposition inputs.
    """



