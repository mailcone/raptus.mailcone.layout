import grok

from mfa_core_filter.interfaces import (
    ISimpleFilterOperator, 
    ISimpleFilterOperatorOperationBased, 
    ISimpleFilterOperatorFuncBased
)

class SimpleFilterOperator(object):
    """ XXX """
    grok.implements(ISimpleFilterOperator)
    grok.provides(ISimpleFilterOperator)
    
    name = None #XXX - doc
    
    def apply(self, filterCondition, source):
        """ XXX """
        pass

class SimpleFilterOperatorOperationBased(SimpleFilterOperator):
    """ XXX """
    grok.implements(ISimpleFilterOperatorOperationBased)
    
class SimpleFilterOperatorFuncBased(SimpleFilterOperator):
    """ XXX """
    grok.implements(ISimpleFilterOperatorFuncBased)
    
    funcName = None #XXX - doc
    
    def apply(self, filterCondition, source):
        """ XXX """
        func = self._getFunction(source)
        funcRes = self._callFunc(func, filterCondition)
        return funcRes
    
    def _getFunction(self, obj):
        """ XXX """
        return obj.__getattribute__(self.funcName)

    def _callFunc(self, func, filterCondition):
        """ XXX """
        return func.__call__(filterCondition)

class SimpleFilterOperatorIs(SimpleFilterOperatorOperationBased, grok.GlobalUtility):
    """ XXX """
    grok.name('is')
    
    name = 'Is'

    def apply(self, filterCondition, source):
        if filterCondition == source:
            return True
        return False

class SimpleFilterOperatorIsNot(SimpleFilterOperatorOperationBased, grok.GlobalUtility):
    """ XXX """
    grok.name('is not')
    
    name = 'Is not'
    
    def apply(self, filterCondition, source):
        if filterCondition != source:
            return True
        return False 

class SimpleFilterOperatorContains(SimpleFilterOperatorFuncBased, grok.GlobalUtility):
    """ XXX """
    grok.name('contains')
    
    name = 'Contains'
    funcName = 'find'

    def apply(self, filterCondition, source):
        """ XXX """
        funcRes = super(SimpleFilterOperatorContains, self).apply(filterCondition, source)
        if funcRes != 0:
            return True
        return False

class SimpleFilterOperatorNotContains(SimpleFilterOperatorFuncBased, grok.GlobalUtility):
    """ XXX """
    grok.name('not contains')
    
    name = 'Does not contains'
    funcName = 'find'

    def apply(self, filterCondition, source):
        """ XXX """
        funcRes = super(SimpleFilterOperatorContains, self).apply(filterCondition, source)
        if funcRes == 0:
            return True
        return False

class SimpleFilterOperatorBeginsWith(SimpleFilterOperatorFuncBased, grok.GlobalUtility):
    """ XXX """
    grok.name('begins with')
    
    name = 'Begins with'
    funcName = 'startswith'

    def apply(self, filterCondition, source):
        """ XXX """
        funcRes = super(SimpleFilterOperatorContains, self).apply(filterCondition, source)
        return funcRes

class SimpleFilterOperatorEndsWith(SimpleFilterOperatorFuncBased, grok.GlobalUtility):
    """ XXX """
    grok.name('ends with')
    
    name = 'Ends with'
    funcName = 'endswith'

    def apply(self, filterCondition, source):
        """ XXX """
        funcRes = super(SimpleFilterOperatorContains, self).apply(filterCondition, source)
        return funcRes