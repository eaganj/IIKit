from IIKit import *
from StateMachines import *
from InstrumentManager import InstrumentManager

import copy
import re

class SubstanceEvent(Event):
    def __init__(self, *args, **kw):
        '''
        SubstanceEvents are either created as Prototypes for a StateMachine, in which case they are called
        with no `args` but may have `kwargs` ; or as actual events to be processed by a State Machine,
        in which case they are called with a raw device event, the emitting device, and a namespace as 
        the only `args`.
        '''
        if args:
            # Wrap an event
            assert len(args) == 3
            rawEvent, device, namespace = args
            self.rawEvent = rawEvent
            self.device = device
            self.namespace = namespace
        else:
            self.options = copy.copy(kw)
        
        super(SubstanceEvent, self).__init__(self.__class__)
        
    def match(self, transition):
        # First check if a device was specified in the transition
        if 'device' in transition.kwargs:
            return transition.kwargs['device'] == self.device
        else:
            return True


class Pointing(SubstanceEvent):
    def getPoint(self):
        # FIXME: This assumes rawEvent is an OSC pointing event
        assert len(self.rawEvent) > 2
        return self.rawEvent[2]
    
    point = property(getPoint)

class ButtonPress(SubstanceEvent):
    pass
    
class ButtonRelease(SubstanceEvent):
    pass

class OSCEvent(SubstanceEvent):
    pass


trailing_numbers_re_str = r'\d+$'
trailing_numbers_re = re.compile(trailing_numbers_re_str)

def substanceOSCEventWrapper(event):
    assert len(event) > 1
    binding, signature = event[0], event[1]
    slash = binding.find('/', 1)
    device = binding[:slash]
    binding = binding[slash+1:]
    binding = trailing_numbers_re.sub('', binding)
    # print "OSC device:", device, "binding:", binding, "signature:", signature
    
    if binding == 'button':
        # Special case buttons to distinguish between ButtonPress and ButtonRelease
        assert len(event) > 2
        payload = event[2]
        etype = (binding, payload)
    else:
        etype = (binding, signature)
    
    if etype in _eventMap:
        eventClass = _eventMap[etype]
        return eventClass(event, device, 'fr.lri.insitu.wild.substance.osc'), None
    else:
        return SubstanceEvent(event), None


InstrumentManager.registerEventWrapper(substanceOSCEventWrapper, 'fr.lri.insitu.wild.substance.osc')

# TODO:
# InstrumentManager.registerEventWrapper(substanceEventWrapper, 'fr.lri.insitu.wild.substance')
    
_eventMap = { 
               ('pointing', 'ff'): Pointing,
               ('button', '0'): ButtonPress,
               ('button', '1'): ButtonRelease,
            }

__all__ = [ clsName for clsName, cls in locals().items() \
                if isinstance(cls, type) and issubclass(cls, SubstanceEvent) ] \
                    + [ 'substanceOSCEventWrapper', ]