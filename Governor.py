
class Governor(object):
    ''' A governor is concerned with gently enforcing the state of objects and with proposing possible actions
        that can be performed on them.  It works in collaboration with Instruments.  That is, it operates
        cooperatively rather than as an enforcer.  When an Instrument is about to perform an action, it can
        query the Governor for proposed alternative actions or alternative parameters to an action, but it is
        not required to.  Likewise, after an Instrument has performed an action, it should, but is not required
        to, notify the Governor of the action performed.  This notification gives the governor a chance to
        react to such changes.  If an Instrument does not provide such a notification, it is effectively 
        disabling the governor's enforcement of its policies for that particular action.
    '''
    def __init__(self, domain):
        self.domain = domain
    
    def availableActions(self, target=None, args=None):
        '''
        Returns a list of actions available for the specified target with the specified parameters.
        '''
        return None
    
    def canPerformActionOnTarget(self, action, target=None, args=None):
        ''' Return True iff the specified `action` with `args` can be performed on the `target`. '''
        return False
    
    def recommendationsForActionOnTarget(self, action, target=None, args=None):
        ''' Returns a sequence of alternate recommendations for action/target/args, including the 
            requested action.
            
            NOTE:  the returned sequence may be a generator.
        '''
        return [ (action, target, args), ]
    
    def actionPerformedOnTarget(self, action, target=None, args=None):
        ''' Notify the governor that the specified action/args has been performed on `target`. '''
        pass


__all__ = ('Governor',)