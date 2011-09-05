import grok
from grokcore import layout

from zope.interface import Interface
from zope.component import getAdapters

from raptus.mailcone.layout import interfaces



grok.templatedir('templates')


class Layout(layout.Layout):
    grok.name('layout')
    grok.context(Interface)

    def update(self):
        providers = getAdapters((self,), interfaces.IResourceProvider)
        for name, provider in providers:
            for resource in provider:
                resource.need()


class Page(layout.Page):
    """ this class do nothing yet!
        for some future project
    """
    
    grok.baseclass()


class Index(Page):
    grok.context(Interface)


class ExceptionPage(layout.ExceptionPage):
    grok.name('index.html')


import zope
class NotFoundPage(layout.NotFoundPage):
    grok.name('index.html')


class UnauthorizedPage(layout.UnauthorizedPage):
    grok.name('index.html')










