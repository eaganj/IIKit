from Instrument import Instrument
from SMInstrument import SMInstrument

class SubstanceInstrumentMixin(object):
    def __init__(self):
        self._context = None
        self.bindings = {}
    
    def getContext(self):
        return self._context
    
    def setContext(self, context):
        self._context = context
        
    context = property(getContext, setContext)
    
    def getDevices(self):
        if not self.stateMachine:
            return []
        
        result = set([ transition.kwargs['device'] for transition in self.stateMachine.all_transitions()
                            if 'device' in transition.kwargs ])
        return result
    
    def bindLogicalDeviceToActualDevice(self, logicalDevice, actualDevice):
        self.bindings[logicalDevice] = actualDevice
        
class SubstanceInstrument(Facet, Instrument, SubstanceInstrumentMixin):
    @Facet.DEPENDENCY("Scene Graph", "The Scene Graph of the WILD Universe")
    def __init__(self):
        # We have to initialize the instrument first to make sure that the Facet can properly introspect
        # itself.
        Instrument.__init__(self)
        Facet.__init__(self, "Instrument")
        SubstanceInstrumentMixin.__init__(self)
        
    def instantiate(self, with_state):
        assert not hasattr(self, 'sg'), "Instrument already has a 'sg' member (cannot install Scene Graph)"
        self.sg = local.get_dependency(self, "Scene Graph")

class SubstanceSMInstrument(Facet, SMInstrument, SubstanceInstrumentMixin):
    @Facet.DEPENDENCY("Scene Graph", "The Scene Graph of the WILD Universe")
    def __init__(self):
        # We have to initialize the instrument first to make sure that the Facet can properly introspect
        # itself.
        SMInstrument.__init__(self)
        Facet.__init__(self, "Instrument")
        SubstanceInstrumentMixin.__init__(self)
        
    def instantiate(self, with_state):
        assert not hasattr(self, 'sg'), "Instrument already has a 'sg' member (cannot install Scene Graph)"
        self.sg = local.get_dependency(self, "Scene Graph")

__all__ = 'SubstanceSMInstrument SubstanceInstrument'.split()