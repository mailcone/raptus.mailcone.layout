import martian
from martian.error import GrokError

import grokcore.view
import grokcore.viewlet
import grokcore.security
import grokcore.component

from grokcore.view.meta.views import ViewSecurityGrokker, default_view_name
from zope.browsermenu.metaconfigure import menuDirective, menuItemDirective, subMenuItemDirective
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.publisher.interfaces.browser import IBrowserView

from megrok.navigation import directives
from megrok.navigation.util import registerMenuItem
from megrok.navigation.meta import MenuViewGrokker

from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.navigation import LocatorMenuItem



class MenuItemGrokker(ViewSecurityGrokker):
    martian.directive(locatormenuitem)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.viewlet.order)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.component.title, default=u'')
    martian.directive(grokcore.component.description, default=u'')
    martian.directive(
        grokcore.view.require, default="zope.View", name='permission')

    def execute(self, factory, config, permission, order, context=None,
                layer=None, name=u'', locatormenuitem=None, description=u'',
                title=u''):
        if locatormenuitem is None:
            return False
        locatormenu, (locator, title, order, icon, group) = locatormenuitem
        title = title or viewtitle or name 
        if martian.util.check_subclass(permission, grokcore.security.Permission):
            permission =  grokcore.component.name.bind().get(permission)
        item_name = '%s@%s' % (locator.__identifier__, name)
        item_itf = directives.itemsimplement.bind().get(locatormenu)
        config.action(discriminator=('viewlet', None, layer,
                         IBrowserView, locatormenu, item_name),
                         callable=registerMenuItem,
                         args=(factory.module_info, LocatorMenuItem, (None, layer, IBrowserView, locatormenu)
                               , item_name, permission, item_itf, layer, 
                               {'title':title,
                                'viewName':name,
                                'description':description,
                                '_icon':icon,
                                'group': group,
                                'locator': locator
                                },
                                (order, MenuViewGrokker._dynamic_items),
                                )
                         )
        MenuViewGrokker._dynamic_items+=1
        return True
