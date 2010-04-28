from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

from Instrument import *
from InstrumentManager import *

class ScottyPickerInstrument(Instrument):
    name = u"Object picker"
    verb = u"Pick object"
    
    def __init__(self):
        super(ScottyPickerInstrument, self).__init__()
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
    
    @classmethod
    def run(cls):
        picker = cls()
        picker.action = lambda picked: setattr(picker, '_picked', picked)
        InstrumentManager.sharedInstrumentManager().activateInstrumentOnce_(picker)
        app = NSApp()
        
        # Block until picked
        try:
            while picker.isActive() and app.isRunning():
                event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                    NSUIntegerMax,#NSAnyEventMask,
                    None,
                    NSDefaultRunLoopMode,
                    True)

                if event is None:
                    continue

                # Abort if user presses ^C
                if (event.type() == NSKeyDown):# and (event.window() == window):
                    chr = event.charactersIgnoringModifiers()
                    if chr == 'c' and (event.modifierFlags() & NSControlKeyMask):
                        raise KeyboardInterrupt

                app.sendEvent_(event)
        finally:
            if picker.isActive():
                picker.deactivate()
        
        return picker._picked
    
    def objectAtPointInWindow(self, point, window):
        ''' 
        Return the object, if any, at `point`. 
        
        If `window` is None, `point` is expressed in screen coordinates.  Otherwise, `point` is taken to
        be in that window's coordinates.
        
        Subclasses are exprected to override this method to provide object-picking behavior.
        '''
        return None
        
    def objectForMouseEvent(self, event):
        ''' Return the object to pick under the mouse.  By default this is the deepest widget under
            the mouse.  
            
            Subclasses can override this method to change the object-picking behavior.  By default, this
            method defers picking to `objectAtPointInWindow()`.  This method should only be overridden
            if any special event-based handling is needed.
        '''
        return self.objectAtPointInWindow(event.locationInWindow(), event.window())
        
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