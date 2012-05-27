import grok
from grokcore import message

from zope import component
from zope.i18n import translate
from zope.interface import Interface
from zope.interface.common.interfaces import IException
from zope.app.security.interfaces import IAuthentication

from raptus.mailcone.settings.interfaces import ILogoLocator

from raptus.mailcone.layout import navigation


grok.templatedir('templates')
grok.context(Interface)



class HeaderManager(grok.ViewletManager):
    grok.name('header')



class ContentBeforeManager(grok.ViewletManager):
    grok.name('content.before')



class ContentManager(grok.ViewletManager):
    grok.name('content')



class ContentAfterManager(grok.ViewletManager):
    grok.name('content.after')



class NavigationManager(grok.ViewletManager):
    grok.name('navigation')



class FooterManager(grok.ViewletManager):
    grok.name('footer')



class Logo(grok.Viewlet):
    grok.viewletmanager(HeaderManager)
    
    @property
    def logo(self):
        logo = component.getUtility(ILogoLocator)()
        if logo.image is None:
            return self.static.get('mailcone.png')
        else:
            return '%s/image/index.html'%grok.url(self.request, logo)
    
    @property
    def homelink(self):
        return grok.url(self.request, grok.getSite())



class Footer(grok.Viewlet):
    grok.viewletmanager(FooterManager)



class MainNavigation(grok.Viewlet):
    grok.viewletmanager(NavigationManager)



class HeaderNavigation(grok.Viewlet):
    grok.viewletmanager(HeaderManager)
    
    @property
    def username(self):
        principal = component.queryUtility(IAuthentication).authenticate(self.request)
        if principal is None:
            return None
        return principal.title



class Message(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(ContentBeforeManager)
    
    @property
    def messages(self):
        li = list()
        source = component.getUtility(message.IMessageSource, name='session')
        for msg in source.list():
            msg.prepare(source)
            li.append(translate(msg.message, context=self.request))
        return li



class ExceptionLogo(grok.Viewlet):
    grok.viewletmanager(ContentBeforeManager)
    grok.context(IException)




