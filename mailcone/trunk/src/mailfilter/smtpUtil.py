import grok

import smtplib

from mailfilter.interfaces import ISmtpServerUtil

# XXX - must be done in a local utility if smtp should be configurable
class SmtpServerUtil(grok.LocalUtility):
    """ XXX """
    grok.implements(ISmtpServerUtil)
    grok.provides(ISmtpServerUtil)
    
    host = ''
    email = ''
    user = ''
    passwd = ''
    authrequeried = ''
    
    def _addHeader(self):
        """ not provided yet - maybe in future versions """

    def send(self, mail):
        """ send given mail obj over configured smtp host """
        mail['From'] = self.email
        smtpObj = smtplib.SMTP(self.host)
        if self.authrequeried:
            smtpObj.login(self.user, self.passwd)
        smtpObj.sendmail(self.email, mail['To'], mail.as_string())
        
    def _addFooter(self):
        """ not provided yet - maybe in future versions """