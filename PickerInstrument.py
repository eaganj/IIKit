from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

from Instrument import *
from InstrumentManager import *

class ScottyPickerInstrument(Instrument):
    def __init__(self, instrumentID):
        super(ScottyPickerInstrument, self).__init__(instrumentID)
        self.name = u"Pick object"
        self.highlightFillColor = 'pink'
        self.highlightBorderColor = 'red'
        self.reset()
    
    def reset(self):
        #self._window = None
        #self._widget = None
        self._object = None
    
    def activate(self):
        super(ScottyPickerInstrument, self).activate()
        self.reset()
    
    def objectForMouseEvent(self, event):
        ''' Return the object to pick under the mouse.  By default this is the deepest widget under
            the mouse.  Subclasses can override this method to change the object-picking behavior.
        '''
        return None
        
    @jre.debug.trap_exceptions
    def mouseMoved(self, event):
        if not self.active:
            return
        
        oldObj = self._object
        obj = self.objectForMouseEvent(event)
        self._object = obj
        if obj and obj != oldObj:
            self.hoverOnObject(obj)

    def mouseDown(self, event):
        pass

    def mouseUp(self, event):
        if not self._active:
            return
        
        obj = self.objectForMouseEvent(event)
        self._object = obj
        if obj:
            self.pickObject(obj)
    
    def highlightsOnHover(self):
        return True
    
    def newGlassViewForGlassWindow(self, window):
        ''' Subclasses can override this to provide a proper PickerGlassView (see ScottyPickerGlassView).'''
        return None
    
    def shouldHijackInteraction(self):
        return True
    
    def highlightObject(self, obj):
        # FIXME: Need to add object protocol support!
        if hasattr(obj, 'window') and hasattr(obj, 'frame'):
            #self.glassViewForWindow(obj.window()).addHighlightBoxForObject_(obj)
            glassView = InstrumentManager.sharedInstrumentManager().glassViewForWindow(obj.window())
            glassView.addHighlightBoxForObject_(obj)
        else:
            print 'Cannot highlight object:', obj
        
    def hoverOnObject(self, obj):
        if self.highlightsOnHover():
            self.highlightObject(obj)
    
    def pickObject(self, obj):
        self.performActionOn(obj)
        
    
PickerInstrument = ScottyPickerInstrument

__all__ = 'ScottyPickerInstrument PickerInstrument'.split()