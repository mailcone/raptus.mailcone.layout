import grok

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import (
    IBaseSettingObject, 
    IActionSettingObject,
    IFilterSettingObject
)

class BaseSettingObject(grok.Container, SearchableContentMixin):
    """ XXX """
    grok.implements(IBaseSettingObject)
    
    title = None
    form_name = None
    
    def getTitle(self):
        """ XXX """
        return self.title
    
    def getFormName(self):
        """ XXX """
        return self.addform_name

class ActionSettingObject(BaseSettingObject):
    """ XXX """
    grok.implements(IActionSettingObject)

class FilterSettingObject(BaseSettingObject):
    """ XXX """
    grok.implements(IFilterSettingObject)