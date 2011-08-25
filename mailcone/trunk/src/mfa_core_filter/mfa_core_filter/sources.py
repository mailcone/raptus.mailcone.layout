import grok

from mfa_core_filter.interfaces import IMailSource

class MailSourceBase(object):
    """ XXX """
    grok.implements(IMailSource)
    
    def getSource(self, obj):
        """ XXX """
        return obj.__getattribute__(self.attrName)
    
class HeaderMailSource(MailSourceBase, grok.GlobalUtility):
    """ XXX """
    grok.name('header')
    
    name = 'Header'
    attrName = 'header'
    
class FromMailSource(MailSourceBase, grok.GlobalUtility):
    """ XXX """
    grok.name('from')

    name = 'From'
    attrName = 'mail_from'

class FromDomMailSource(MailSourceBase, grok.GlobalUtility):
    """ XXX """
    grok.name('from_domain')
    
    name = 'From domain'
    attrName = 'mail_from_domain'

class ToMailSource(MailSourceBase, grok.GlobalUtility):
    """ XXX """
    grok.name('to')
    
    name = 'To'
    attrName = 'mail_to'

class ToDomMailSource(MailSourceBase, grok.GlobalUtility):
    """ XXX """
    grok.name('to_domain')
    
    name = 'To domain'
    attrName = 'mail_to_domain'

class CcMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('cc')
    
    name = 'Cc'
    attrName = 'mail_cc'

class DateMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('date')
    
    name = 'Date'
    attrName = 'date'

class SizeMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('mail size')
    
    name = 'Mail size'
    attrName = ''

class BodyMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('body')
    
    name = 'Body'
    attrName = 'content'

class AttachmentMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('attachment')
    
    name = 'Attachment'
    attrName = ''

class FilenameMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('filename')
    
    name = 'Filename'
    attrName = ''

class FilesizeMailSource(MailSourceBase, grok.GlobalUtility):
    """XXX"""
    grok.name('file size')
    
    name = 'File size'
    attrName = ''