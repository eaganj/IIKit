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

from Object import Object

class Action(Object):
    def __init__(self, protocols=None):
        super(Action, self).__init__()

        if not protocols:
            protocols = []
            
        self.protocols = protocols

    ### FIXME: Not used!
    @classmethod
    def requiredProtocols(cls):
        return []
    
    @classmethod
    def optionalProtocols(cls):
        return []

    def __call__(self, target, *args):
        self._validateTargetForProtocols(target)
    
    def _validateTargetForProtocols(self, target): # FIXME: raise on non-conformability
        for protocol in self.protocols:
            if not self._validateTargetForProtocol(target, protocol):
                return False
        
        return True
    
    def _validateTargetForProtocol(self, target, protocol):
        return protocol.objectConforms()
    

__all__ = 'Action'.split()