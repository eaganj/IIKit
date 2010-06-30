from Instrument import *
from StateMachines import *

class SMInstrument(Instrument, statemachine):
    def __init__(self):
        super(SMInstrument, self).__init__()
        #Instrument.__init__(self)
        #statemachine.__init__(self)
         
        self.stateMachine = self
    
    def setStateMachine(self, machine):
        self._stateMachine = machine
        if machine:
            machine.instrument = self
    
    def getStateMachine(self):
        return self._stateMachine
        
    stateMachine = property(getStateMachine, setStateMachine)
    

#class InstrumentStateMachine(statemachine):
#    def __init__(self, instrument):
#        self._instrument = instrument
#    
#    def 

#class SMInstrument(Instrument):
#    def __init__(self, instrumentID):
        