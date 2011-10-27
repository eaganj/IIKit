# -*- coding: utf-8 -*-
#
# IIKit -- the Instrumental Interaction Toolkit
# Copyright 2009-2011, Université Paris-Sud
# by James R. Eagan (code at my last name dot me)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

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
        