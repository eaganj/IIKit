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

print "import PickerInstrument"

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

from Instrument import *
from InstrumentManager import *
# from IIKit import InstrumentContext

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
    
    def activate(self, context=None):
        super(ScottyPickerInstrument, self).activate(context)
        self.reset()
    
    @classmethod
    def run(cls):
        from IIKit import InstrumentContext
        picker = cls()
        picker.action = lambda picked: setattr(picker, '_picked', picked)
        context = InstrumentContext()
        InstrumentManager.sharedInstrumentManager().activateInstrument_withContext_once_(picker, 
                                                                                         context, 
                                                                                         True)
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
        if self.context and hasattr(obj, 'window') and hasattr(obj, 'frame'):
            #self.glassViewForWindow(obj.window()).addHighlightBoxForObject_(obj)
            # glassView = InstrumentManager.sharedInstrumentManager().glassViewForWindow(obj.window())
            glassWindow = self.context.glassWindows.get(obj.window(), None)
            glassView = glassWindow.contentView() if glassWindow else None
            if glassView:
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