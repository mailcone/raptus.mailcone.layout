import grok
from zope.component import getMultiAdapter

from mfa_core_filter.interfaces import IFilterContainer
from mailfilter.viewletmanagers import Main
from mfa_complexmatchfilter.interfaces import IComplexMatchFilter
from mfa_complexmatchfilter.contents import ComplexMatchFilter

class AddComplexMatchFilterView(grok.View):
    """ Provide view container for viewlet which contains the generate add form """
    grok.context(IFilterContainer)
    grok.template('master')
    grok.name('addComplexMatchFilter')
    grok.require('mailfilter.view')

class AddComplexMatchFilterViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form AddComplexMatchFilterForm """
    grok.viewletmanager(Main)
    grok.context(IFilterContainer)
    grok.view(AddComplexMatchFilterView)

    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='addcomplexmatchfilterform')
        self.form.update_form()

    def render(self):
        return self.form.render()

class ComplexMatchFilterView(grok.View):
    """ View for complex match filter - redirect to parent object view """
    grok.context(IComplexMatchFilter)
    grok.name('index')
    grok.template('master')
    grok.require('mailfilter.view')
    
class ComplexMatchFilterViewlet(grok.Viewlet):
    """ XXX """
    grok.context(IComplexMatchFilter)
    grok.template('complexmatchfilter_viewlet')
    grok.viewletmanager(Main)
    grok.view(ComplexMatchFilterView)

class ComplexMatchFilterMacro(grok.View):
    """ Provide an html snippet for complex match filters """
    grok.context(IComplexMatchFilter)
    grok.name('macro')
    grok.template('complexmatchfilter_macro')
    grok.require('mailfilter.view')

class EditComplexMatchFilterView(grok.View):
    """ Provide view container for viewlet which contains the generate edit form """
    grok.context(IComplexMatchFilter)
    grok.name('edit')
    grok.template('master')
    grok.require('mailfilter.view')

class EditComplexMatchFilterViewlet(grok.Viewlet):
    """ provide viewlet for the generate edit form EditComplexMatchFilterForm """
    grok.viewletmanager(Main)
    grok.context(IComplexMatchFilter)
    grok.view(EditComplexMatchFilterView)
    
    def update(self):
        self.form = getMultiAdapter((self.context, self.request), name='editcomplexmatchfilterform')
        self.form.update_form()

    def render(self):
        return self.form.render()
    
class DeleteComplexMatchFilterView(grok.View):
    grok.context(IComplexMatchFilter)
    grok.name('delete')
    grok.require('mailfilter.view')
    
    parent = None
    
    def update(self):
        self.parent = self.context.__parent__
        self.parent.delFilter(self.context)
    
    def render(self):
        self.redirect(self.url(self.parent))