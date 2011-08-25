# grok stuff
import grok
from grok import index

from mailfilter.app import MailfilterApp
from mailfilter.interfaces import ISearchableContent

class ContentIndexes(grok.Indexes):
    """
        Sitewide indexes for objects providing IBaseSearchable
    """
    grok.site(MailfilterApp)
    grok.context(ISearchableContent)
    grok.name ('catalog')

    content_type = index.Field(attribute='content_type')
    id = index.Field(attribute='id')
    parent_url = index.Field(attribute='parent_url')
    implements = index.Set(attribute='implements')
    sortNr = index.Field(attribute='sortNr')