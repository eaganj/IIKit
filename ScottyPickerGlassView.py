from __future__ import with_statement
#######
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