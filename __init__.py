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

'''
IIKit -- the Instrumental Interaction Toolkit
Created by James R. Eagan <eaganj@lri.fr> (www.eagan.me)

The goal of IIKit is to help facilitate the creation of instrumental interaction-based user interfaces.  It is based on the concepts described in Beaudoin-Lafon's Instrumental Interaction (2000) paper and Klokmose's VIGO (2009) paper.

The basic entities in the IIKit are:
    * Protocols, which describe an object's interface
    * Actions, which perform higher-level logical operations on objects
    * Governors, which maintain object state constraints and may suggest Actions
    * Instruments, which describe how to transform user input into actions on objects and/or user output
    * Instrument Managers, which are (or should be) themselves Instruments tasked with managing instrument activation and deactivation, event dispatch, etc.
    * GlassWindows, which provide transparent graphical overlays to draw on top of existing graphical views.

IIKit provides an abstract base implementation for the above entities.  There are two currently supported concrete implementations: one for Scotty, and one for Substance.  

Scotty integrates with Cocoa applications on Mac OS X, allowing the integration of instruments on a per-application basis.  It is intented to be imported as `from IIKit.scotty import *`.  For more information, refer to the Scotty injector documentation.

IIKit Substance support integrates with the Shared Substance Canvas environment to provide instrumental interaction in a distributed environment.  It can be imported via `from IIKit.Substance import *`.  Refer to the Substance Canvas Master demos for examples of its use.
'''

from Object import *
from tag import *
from selectionManager import *
from selectionTag import *
from selectionInfo import *
from action import *
from protocol import *
from Governor import *
from Instrument import *
from SMInstrument import *
from InstrumentContext import *
from InstrumentLoader import *
from InstrumentManager import *
from GlassWindow import *
from PickerInstrument import *