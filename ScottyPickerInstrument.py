from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

import PickerInstrument
from ScottyPickerGlassView import *

class ScottyPickerInstrument(PickerInstrument.PickerInstrument):
    def __init__(self, instrumentID):
        super(ScottyPickerInstrument, self).__init__(instrumentID)
        self.highlightFillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.125)
        self.highlightBorderColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.25)
    
    def newGlassViewForWindow(self, window):
        return ScottyPickerGlassView(window.frame(), self)

PickerInstrument.PickerInstrument = ScottyPickerInstrument
PickerInstrument = ScottyPickerInstrument

__all__ = 'ScottyPickerInstrument PickerInstrument'.split()