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

from __future__ import with_statement

import jre.debug

from collections import deque

from InstrumentManager import *
import Object

# TODO:  Make GlassWindow itself an instrument
class IIKitGlassWindow(Object.Object):
    ''' A glass window is a transparent overlay that can be attached to an existing object, such as a widget,
        window, or the full screen.  It acts as a child of this object, following it as its position updates.
        Glass windows are useful for drawing annotations on top of an existing widget or even replacing its 
        appearance entirely.  They can also optionally intercept and redirect input events, transforming the
        behavior of the parent object.
        
        FIXME:  The GlassWindow interface is currently in transition.
    '''
    def __init__(self, parent=None):
        ''' Create a new glass window attached to `parent`.  If no parent is provided, then a fulllscreen
            glass window is created instead.
        '''
        super(IIKitGlassWindow, self).__init__()
        pass # OVERRIDE IN SUBCLASSES
        
        self._hijacksMouseInteraction = False
    
    def resetEventsMask(self):
        pass # OVERRIDE IN SUBCLASSES
        
    def setHijacksInteraction_(self, hijack):
        self._hijacksMouseInteraction = hijack
    
    def reset(self):
        pass # OVERRIDE IN SUBCLASSES
        
GlassWindow = IIKitGlassWindow
        
__all__ = 'GlassWindow'.split()