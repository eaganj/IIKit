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

print "import ScottyInstrumentContext"

from AppKit import *
from Foundation import *
import objc

import InstrumentContext
from ScottyController import Scotty
from ScottyGlassWindow import GlassWindow

class ScottyInstrumentContext(InstrumentContext.IIKitInstrumentContext):
    def attachGlassWindowToActivationSource(self, interactive=True):
        if self.activationSource:
            parentWindow = self.activationSource.window()
            if not parentWindow:
                return None
            
            return self.attachGlassWindowToWindow(parentWindow, interactive)
        else:
            return None
    
    def attachGlassWindowToAllWindows(self, interactive=True):
        # FIXME : Add support for background windows, too.
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
    
    def attachGlassWindowToWidget(self, parentWidget, interactive=True):
        raise Exception(u"Not implemented")
    
    def glassViewForWindow(self, parentWindow):
        glassWindow = self.glassWindows.get(parentWindow, None)
        if glassWindow:
            return glassWindow.contentView()
        return None
    
    def instrumentWasDeactivated(self, instrument):
        for parentWindow, glassWindow in self.glassWindows.items():
            # print "clobber", glassWindow, "of", parentWindow
            glassWindow.orderOut_(None)
        
        # FIXME : For some reason, this causes an NSAutoreleasePool double drain warning.  Is this a bug
        # here or in PyObjC? -JRE 10.7.2 stock
        # self.glassWindows.clear() # This should be uncommented to avoid a potential mem leak, right? -JRE

InstrumentContext.InstrumentContext = ScottyInstrumentContext
InstrumentContext = ScottyInstrumentContext

__all__ = 'InstrumentContext ScottyInstrumentContext'.split()