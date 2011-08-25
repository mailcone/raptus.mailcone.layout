import grok

import logging
import os

from zope.component import getUtility
from zope import event, lifecycleevent

from mailfilter.app import SearchableContentMixin
from mailfilter.interfaces import ISearchableContent
from mfa_core_action.interfaces import IAction, IActionType, IActionContainer
from mfa_writelogaction.interfaces import IWriteLogAction, ILogfile, IWriteLogActionSettingObject, ILogfileManager

class WriteLogAction(grok.Model, SearchableContentMixin):
    """ Provide a action for write messages in logfiles """
    grok.implements(IWriteLogAction, IAction, ISearchableContent)
    grok.context(IActionContainer)

    id = None
    content_type = 'WriteLogAction'
    sortNr = None
    
    def __init__(self, id, logfile, loglevel, logmessage, match):
        """ Constructor """
        super(WriteLogAction, self).__init__()
        self.id = id
        self.logfile = logfile
        self.loglevel = loglevel
        self.logmessage = logmessage
        self.match = match

    def setSortNr(self, number):
        """XXX"""
        self.sortNr = number
        #reindexing
        event.notify(
            lifecycleevent.ObjectModifiedEvent(self, 
                                               lifecycleevent.Attributes(IWriteLogAction, 'sortNr')
            )
        )
        
    grok.traversable('moveUp')
    def moveUp(self):
        return self.__parent__.moveActionUp(self)

    grok.traversable('moveDown')
    def moveDown(self):
        return self.__parent__.moveActionDown(self)

    def getActionTypeTitle(self):
        """ return title for registered filter type """
        return getUtility(IActionType, "WriteLogActionType").title
    
    def apply(self):
        """ XXX """
        manager = getUtility(ILogfileManager)
        logObj = manager.getLogfileById(self.logfile) 

        log = logging.getLogger (logObj.name)
        log.setLevel (logging.INFO)
        lformatter = logging.Formatter('%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        lhandler = logging.FileHandler(logObj.getLogfile())
        lhandler.setFormatter(lformatter)
        log.addHandler(lhandler)

        #XXX - must be solved better           
        if self.loglevel == 'info':
            log.info(self.logmessage)
        if self.loglevel == 'warning':
            log.warning(self.logmessage)
        if self.loglevel == 'error':
            log.error(self.logmessage)
        
        log.removeHandler(lhandler)    
        lhandler.close()

class Logfile(grok.Container, SearchableContentMixin):
    """ Define a logfile - used by WriteLogAction """
    grok.context(IWriteLogActionSettingObject)
    grok.implements(ILogfile, ISearchableContent)
    
    id = None
    name = None
    logfile = None
    logpath = None
    
    def __init__(self, name, logfile, filepath):
        """ Constructor """
        super(Logfile, self).__init__()
        self.id = name.replace(' ', '-') # XXX - really simple, could be done better
        self.name = name
        self.logfile = logfile
        self.filepath = filepath
        
    def getLogfile(self):
        """ check if logfile exists return only path to logfile, 
            else create logfile and return path """
        file = ''
        if self.logfile[-4:] != '.log':
            file = self.logfile + '.log'
        else:
            file = self.logfile
             
        filepath = os.path.join (self.filepath, file)
        if not os.path.isfile (filepath):
            self.createLogfile(filepath)
        return filepath
        
    def createLogfile(self, file):
        """ XXX """
        file = open (file, 'w')
        file.close ()