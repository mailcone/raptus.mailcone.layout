import os
import json
import grok

from grokcore.view.interfaces import ITemplateFileFactory

from hurry.query import query,set

from zope.component import getUtility

from raptus.mailcone.layout import _

grok.templatedir('templates')


class BaseDataTable(grok.View):
    """ This class provide a base for the js.jquery_datatables.
        Two parts of view are supported by this view:
            1. the html output for included by a custom template
            2. a view for loading all data over ajax
    """
    
    grok.baseclass()
    
    interface_fields = None
    ignors_fields = list()
    actions = tuple()
    
    def _fields(self):
        # dict() dosen't work because a wrong ordering
        li = list()
        for fi in grok.AutoFields(self.interface_fields).omit(*self.ignors_fields):
            li.append((fi.field.getName(), fi.field.title,))
        return li

    def _linkbuilder(self, action, brain):
        href = '%s/%s' % (grok.url(self.request, brain), action.get('link'),)
        ac = dict(href=href)
        ac.update(action)
        return '<a href="%(href)s" class="ui-table-action %(cssclass)s" title="%(title)s">%(title)s</a>' % ac
    
    def _aaData(self, brains):
        results = list()
        for brain in brains:
            row = list()
            for field, title in self._fields():
                row.append(getattr(brain, field, None))
            for ac in self.actions:
                row.append(self._linkbuilder(ac, brain))
            results.append(row)
        return results
    
    def _iTotalDisplayRecords(self, brains):
        return len(brains)
    
    def _iTotalRecords(self, brains):
        return len(brains)
    
    def _sEcho(self, brains):
        return int(self.request.get('sEcho', 1))
    
    def _metadata(self, brains):
        di = dict();
        di['ajaxcontent'] = self._ajaxcontent(brains)
        return di
    
    def _ajaxcontent(self, brains):
        li = list()
        for brain in brains:
            li.append(grok.url(self.request, brain))
        return li
    
    def render(self):
        
        if self.interface_fields is None:
            raise NotImplementedError('you must override interface_fields in your subclass!')
        
        iDisplayLength = int(self.request.form.get('iDisplayLength',0))
        iDisplayStart = int(self.request.form.get('iDisplayStart',0))
        sSearch = self.request.form.get('sSearch','')
        iSortCol_0 = int(self.request.form.get('iSortCol_0',-1))
        sSortDir_0 = self.request.form.get('sSortDir_0','')
        sortcol = (iSortCol_0 < len(self._fields()) and iSortCol_0 >= 0) and ('catalog',self._fields()[iSortCol_0][0],) or None
        sorddir = sSortDir_0 == 'asc' and True or False
        

        queryutil = getUtility(query.interfaces.IQuery)
        
        queries = []
        if sSearch:
            queries.append(query.Text(('catalog', 'text'), '*'+'* *'.join(sSearch.split(' '))+'*'))
        queries.append(set.AnyOf(('catalog', 'implements'), [self.interface_fields.__identifier__,]))
        
        brains = queryutil.searchResults(query.And(*queries),
                                         reverse=sorddir,
                                         sort_field=None,)
        limited = [i for i in brains][iDisplayStart:iDisplayStart+iDisplayLength]
        
        results = dict()
        results['aaData'] = self._aaData(limited)
        results['iTotalRecords'] = self._iTotalRecords(brains)
        results['iTotalDisplayRecords'] = self._iTotalDisplayRecords(brains)
        results['sEcho'] = self._sEcho(brains)
        results['metadata'] = self._metadata(brains)
        
        return json.dumps(results)
        
    def html(self):
        template = os.path.join(os.path.dirname(__file__),'templates','datatable.cpt')
        return getUtility(ITemplateFileFactory, name='cpt')(filename=template).render(self)

    @property
    def id(self):
        return self.__view_name__
    
    @property
    def ajaxurl(self):
        return self.url()
    
    @property
    def columns(self):
        return [ v for k, v in self._fields()]
    
    @property
    def tabletools(self):
        return json.dumps(dict(aButtons=list()))
        
        
        
        
        
        