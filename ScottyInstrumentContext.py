from __future__ import with_statement

from AppKit import *
from Foundation import *
import objc

import InstrumentContext
from ScottyController import Scotty
from ScottyGlassWindow import GlassWindow

class ScottyInstrumentContext(InstrumentContext.IStarInstrumentContext):
    def attachGlassWindowToActivationSource(self, interactive=True):
        if self.activationSource:
            parentWindow = self.activationSource.window()
            if not parentWindow:
                return None
            
            return self.attachGlassWindowToWindow(parentWindow, interactive)
        else:
            return None
    
    def attachGlassWindowToAllWindows(self, interactive=True):
        glassWindows = [ self.attachGlassWindowToWindow(window, interactive) for window in NSApp().windows()
                            if not isinstance(window, (GlassWindow,)) ]
        return glassWindows
    
    def attachGlassWindowToWindow(self, parentWindow, interactive=True):
        glassWindow = GlassWindow(parentWindow)
        self.glassWindows[parentWindow] = glassWindow
        
        # Hook into the responder chain
        if interactive:
            glassWindow.setHijacksInteraction_(True)
            keyWindow = NSApp().keyWindow()
            if keyWindow:
                if keyWindow.firstResponder():
                    nextResponder = keyWindow.firstResponder()
                else:
                    nextResponder = keyWindow
                glassWindow.setNextResponder_(nextResponder)
        
            # Take key focus
            glassWindow.makeKeyWindow()
        
        return glassWindow
    
    def glassViewForWindow(self, parentWindow):
        glassWindow = self.glassWindows.get(parentWindow, None)
        if glassWindow:
            return glassWindow.contentView()
        return None

InstrumentContext.InstrumentContext = ScottyInstrumentContext
InstrumentContext = ScottyInstrumentContext

__all__ = 'InstrumentContext ScottyInstrumentContext'.split()