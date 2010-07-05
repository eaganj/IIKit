from IIKit import *
from StateMachines import *
from InstrumentManager import InstrumentManager

import copy
import re

import jre.debug

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
            # print "-> args:", args
            assert len(args) == 4
            rawEvent, device, binding, namespace = args
            self.rawEvent = rawEvent
            self.device = device
            self.binding = binding
            self.namespace = namespace
        else:
            self.options = copy.copy(kw)
        
        super(SubstanceEvent, self).__init__(self.__class__)
        
    def match(self, transition):
        # First check if a device was specified in the transition
        logical_device = transition.kwargs.get('device', None)
        if logical_device:
            if logical_device == '<bound>':
                # Legacy support
                if hasattr(transition.state.state_machine, "deviceID"):
                    if transition.state.state_machine.deviceID == self.device:
                        return True
                return False
            
            instrument = transition.state.state_machine.instrument
            assert instrument is not None
            
            # print "Checking device: (%s)" % (self.device), instrument.bindings.get(self.device, None), "?=?", logical_device
            return instrument.bindings.get(self.device, None) == logical_device
            
        
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
    #device = binding[1:slash]
    device = binding
    binding = binding[slash+1:]
    bindingType = trailing_numbers_re.sub('', binding)
    # print "OSC device:", device, "binding:", binding, "signature:", signature
    
    if bindingType == 'button':
        # Special case buttons to distinguish between ButtonPress and ButtonRelease
        assert len(event) > 2
        payload = event[2][0] if len(event[2]) > 0 else None
        etype = (bindingType, payload)
    else:
        etype = (bindingType, signature)
    
    # print "Mapping on event type:", etype
    if etype in _eventMap:
        eventClass = _eventMap[etype]
        return eventClass(event, device, binding, 'fr.lri.insitu.wild.substance.osc'), None
    else:
        jre.debug.interact()
        return SubstanceEvent(event, device, binding, 'fr.lri.insitu.wild.substance.osc'), None

def substanceViconEventWrapper(event):
    assert len(event) == 2
    binding, point = event
    device = binding
    slash = binding.find('/', 1)
    binding = binding = binding[slash+1:]
    viconEvent = (device, 'ii', point)
    # print "Vicon device:", device, "binding:", binding
    return Pointing(viconEvent, device, binding, 'fr.lri.insitu.wild.substance.vicon'), None

InstrumentManager.registerEventWrapper(substanceOSCEventWrapper, 'fr.lri.insitu.wild.substance.osc')
InstrumentManager.registerEventWrapper(substanceViconEventWrapper, 'fr.lri.insitu.wild.substance.vicon')

# TODO:
# InstrumentManager.registerEventWrapper(substanceEventWrapper, 'fr.lri.insitu.wild.substance')
    
_eventMap = { 
               ('pointing', 'ff'): Pointing,
               ('button', 1): ButtonPress,
               ('button', 0): ButtonRelease,
            }

__all__ = [ clsName for clsName, cls in locals().items() \
                if isinstance(cls, type) and issubclass(cls, SubstanceEvent) ] \
                    + [ 'substanceOSCEventWrapper', ]