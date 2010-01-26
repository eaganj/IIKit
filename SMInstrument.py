from Instrument import *
from StateMachines import *

# class SMInstrument(Instrument, statemachine):
#     def __init__(self, instrumentID):
#         Instrument.__init__(self, instrumentID)
#         statemachine.__init__(self)
#         
#         self.stateMachine = self
#         

class InstrumentStateMachine(statemachine):
    def __init__(self, instrument):
        self._instrument = instrument
    
    def 

class SMInstrument(Instrument):
    def __init__(self, instrumentID):
        