import os
import json
import grok

import datetime

from grokcore.view.interfaces import ITemplateFileFactory

from hurry.query import query,set

from zope.formlib import form
from zope.component import getUtility

from sqlalchemy.sql import and_
from z3c.saconfig import Session
from sqlalchemy import func, desc, asc

from raptus.mailcone.core import utils

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
    select_fields = list()
    actions = tuple()
    inputs = tuple()
    
    def _fields(self):
        # dict() dosen't work because a wrong ordering
        li = list()
        for fi in self._formfields():
            li.append((fi.field.getName(), fi.field.title,))
        return li

    def _formfields(self):
        fields = grok.AutoFields(self.interface_fields).omit(*self.ignors_fields)
        if self.select_fields:
            fields = fields.select(*self.select_fields)
        return fields

    def _linkbuilder(self, action, brain):
        href = '%s/%s' % (self._url(brain), action.get('link'),)
        ac = dict(href=href)
        ac.update(action)
        return '<a href="%(href)s" class="ui-table-action %(cssclass)s" title="%(title)s">%(title)s</a>' % ac
    
    def inputbuilder_value(self, input, brain):
        raise NotImplementedError('you must override inputbuilder_value in your subclass!')

    def _inputbuilder(self, input, brain):
        di = dict(name=brain.id,
                  checked=self.inputbuilder_value(input, brain) and 'checked="checked"')
        di.update(input)
        return '<input type="%(type)s" class="ui-table-input %(cssclass)s" name="%(prefix)s.%(name)s" %(checked)s />' % di
    
    def _aaData(self, brains):
        results = list()
        for brain in brains:
            row = list()
            widgets =form.setUpEditWidgets(self._formfields(), request=self.request,
                                           context=brain, form_prefix='', for_display=True)
            for widget in widgets:
                row.append(widget())
            for ac in self.actions:
                row.append(self._linkbuilder(ac, brain))
            for input in self.inputs:
                row.insert(0, self._inputbuilder(input, brain))
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
            li.append(self._url(brain))
        return li
    
    def _query(self, **request_data):
        queryutil = getUtility(query.interfaces.IQuery)
        queries = []
        sSearch, reverse, sort_field = request_data['sSearch'], request_data['sortdir'], request_data['sortcol']
        if sSearch:
            queries.append(query.Text(('catalog', 'text'), '*'+'* *'.join(sSearch.split(' '))+'*'))
        queries.append(set.AnyOf(('catalog', 'implements'), [self.interface_fields.__identifier__,]))
        brains = queryutil.searchResults(query.And(*queries),
                                         reverse=reverse,
                                         sort_field=sort_field,)
        return brains
    
    def _url(self, brain):
        return grok.url(self.request, brain)
    
    def render(self):
        if self.interface_fields is None:
            raise NotImplementedError('you must override interface_fields in your subclass!')
        request_data = dict()
        request_data['iDisplayLength'] = int(self.request.form.get('iDisplayLength',0))
        request_data['iDisplayStart'] = int(self.request.form.get('iDisplayStart',0))
        request_data['sSearch'] = self.request.form.get('sSearch','')
        request_data['iSortCol_0'] = int(self.request.form.get('iSortCol_0',-1))
        request_data['sSortDir_0'] = self.request.form.get('sSortDir_0','')
        request_data['sortcol'] = (request_data['iSortCol_0'] < len(self._fields()) and request_data['iSortCol_0'] >= 0) and ('catalog',self._fields()[request_data['iSortCol_0']][0],) or None
        request_data['sortdir'] = request_data['sSortDir_0'] == 'asc' and True or False
        
        brains = self._query(**request_data)
        
        iDisplayStart, iDisplayLength = request_data['iDisplayStart'], request_data['iDisplayLength']
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



class BaseDataTableSql(BaseDataTable):
    grok.baseclass()
    
    model = None
    
    def _query(self, **request_data):
        sSearch = request_data['sSearch']
        if self.model is None:
            raise NotImplementedError('you must override model attribute in your subclass!')
        
        query = Session().query(self.model)
        catalog, sortcol = request_data.get('sortcol')
        if sortcol:
            dir = desc
            if request_data['sortdir']:
                dir = asc
            query = query.order_by(dir(getattr(self.model, sortcol)))
        if request_data['sSearch']:
            query=query.filter(self.model.index_searchable.match(request_data['sSearch']))

        self.amount = query.count()

        query = query.offset(request_data['iDisplayStart']).limit(request_data['iDisplayLength'])
        self.query_data = query.all()
        return self.query_data

    def _url(self, brain):
        return '%s/%s' % (self.request.getURL(1), brain.id)


    def _iTotalRecords(self, brains):
        #column_id = self.model.__table__._autoincrement_column
        #(count,) = Session().query(func.count(column_id)).first()
        return self.amount

    def _iTotalDisplayRecords(self, brains):
        return self._iTotalRecords(brains)

    def _aaData(self, brains):
        return super(BaseDataTableSql, self)._aaData(self.query_data)
        
        
        
        