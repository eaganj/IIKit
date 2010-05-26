from Instrument import Instrument
from SMInstrument import SMInstrument

class SubstanceInstrument(Facet, Instrument):
    @Facet.DEPENDENCY("Scene Graph", "The Scene Graph of the WILD Universe")
    def __init__(self):
        # We have to initialize the instrument first to make sure that the Facet can properly introspect
        # itself.
        Instrument.__init__(self)
        Facet.__init__(self, "Instrument")
        
    def instantiate(self, with_state):
        assert not hasattr(self, 'sg'), "Instrument already has a 'sg' member (cannot install Scene Graph)"
        self.sg = local.get_dependency(self, "Scene Graph")

class SubstanceSMInstrument(Facet, SMInstrument):
    @Facet.DEPENDENCY("Scene Graph", "The Scene Graph of the WILD Universe")
    def __init__(self):
        # We have to initialize the instrument first to make sure that the Facet can properly introspect
        # itself.
        SMInstrument.__init__(self)
        Facet.__init__(self, "Instrument")
        
    def instantiate(self, with_state):
        assert not hasattr(self, 'sg'), "Instrument already has a 'sg' member (cannot install Scene Graph)"
        self.sg = local.get_dependency(self, "Scene Graph")

__all__ = 'SubstanceSMInstrument SubstanceInstrument'.split()