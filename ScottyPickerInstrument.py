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

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

import PickerInstrument
from ScottyPickerGlassView import *

class ScottyPickerInstrument(PickerInstrument.PickerInstrument):
    def __init__(self):
        super(ScottyPickerInstrument, self).__init__()
        self.highlightFillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.125)
        self.highlightBorderColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.25)
    
    def newGlassViewForGlassWindow(self, window):
        return ScottyPickerGlassView(window.frame(), self)

PickerInstrument.PickerInstrument = ScottyPickerInstrument
PickerInstrument = ScottyPickerInstrument

__all__ = 'ScottyPickerInstrument PickerInstrument'.split()