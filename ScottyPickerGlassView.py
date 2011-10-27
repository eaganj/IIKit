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

from AppKit import *
from Foundation import *
import objc

import jre.cocoa
import jre.debug

class ScottyPickerGlassView(NSView):
    def __new__(cls, frame, instrument):
        return cls.alloc().initWithFrame_instrument_(frame, instrument)
        
    def initWithFrame_instrument_(self, frame, instrument):
        self = super(ScottyPickerGlassView, self).initWithFrame_(frame)
        if not self:
            return self
        
        self._instrument = instrument
        self.reset()
        
        return self
        
    def addHighlightBoxForObject_(self, widget):
        # FIXME: Add Protocol support
        rect = widget.convertRectToBase_(widget.convertRect_fromView_(widget.frame(), widget.superview()))
        self._rect = rect
        self.setNeedsDisplay_(True)
        
    def reset(self):
        #super(ScottyPickerGlassView, self).reset()
        self._rect = None
        self.setNeedsDisplay_(True)
    
    @jre.debug.trap_exceptions
    def drawRect_(self, rect):
        ## Setup the glass pane
        #NSColor.clearColor().set()
        #NSRectFill(rect)
        
        self.drawWidgetRect()
    
    def drawWidgetRect(self):
        # Stop here if there's nothing to draw
        if not self._rect:
            return
        
        color = self._instrument.highlightFillColor
        color.set()
        NSBezierPath.fillRect_(self._rect)
        color = self._instrument.highlightBorderColor
        color.set()
        NSBezierPath.strokeRect_(self._rect)
    
PickerGlassView = ScottyPickerGlassView

__all__ = 'PickerGlassView ScottyPickerGlassView'.split()