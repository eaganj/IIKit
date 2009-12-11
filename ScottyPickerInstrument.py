from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

from PickerInstrument import *
from ScottyPickerGlassView import *

class ScottyPickerInstrument(PickerInstrument):
    def __init__(self, instrumentID):
        super(ScottyPickerInstrument, self).__init__(instrumentID)
        self.highlightFillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.125)
        self.highlightBorderColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.25)
    
    def newGlassViewForWindow(self, window):
        return ScottyPickerGlassView(window.frame(), self)

__all__ = 'ScottyPickerInstrument'.split()