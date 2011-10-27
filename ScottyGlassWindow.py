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

import GlassWindow as GlassWindowModule
from InstrumentManager import *
from ScottyController import Scotty
from ScottyEventFunnel import *

class ScottyGlassWindow(EventFunnel(NSWindow), GlassWindowModule.GlassWindow):
    def __new__(cls, parent=None):
        if parent:
            return cls.alloc().initWithParent_(parent)
        else:
            return cls.alloc().initFullScreen()
    
    def initWithParent_(self, parent):
        if isinstance(parent, NSWindow):
            parentFrame = parent.frame()
        else:
            # Convert widget frame to screen coords
            parentOrigin = parent.window().convertBaseToScreen_(
                                                    parent.convertRectToBase_(parent.frame()).origin)
            parentFrame = NSMakeRect(parentOrigin.x, parentOrigin.y, *parent.frame().size)
        
        self = self.initWithFrame_(parentFrame)
        if not self:
            return self
        
        if isinstance(parent, NSWindow):
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                                                                           self,
                                                                           self.parentDidResize_,
                                                                           NSWindowDidResizeNotification,
                                                                           parent)
            parent.addChildWindow_ordered_(self, NSWindowAbove)
        else:
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                                                                        self,
                                                                        self.parentDidResize_,
                                                                        NSViewFrameDidChangeNotification,
                                                                        parent)
            # parent.window().addChildWindow_ordered_(self, NSWindowAbove)
        return self
    
    def initFullScreen(self):
        screenFrame = NSScreen.mainScreen().frame() # FIXME: Need to account for multiple screens!
        return self.initWithFrame_(screenFrame)
    
    def initWithFrame_(self, frame):
        print "Init glass window using frame:", frame
        self = super(ScottyGlassWindow, self).initWithContentRect_styleMask_backing_defer_(
                                                frame,
                                                NSBorderlessWindowMask,
                                                NSBackingStoreBuffered,
                                                False
                                                )
        if not self:
            return self
        
        GlassWindowModule.GlassWindow.__init__(self, None)
            
        self._hijacksMouseInteraction = False
        self.reset()
            
        Scotty().registerGlassWindow_(self)
        
        # FIXME : refactor somewhere else
        #decoratorWindow = DecoratorWindow(parent)
        
        return self
    
    @classmethod
    def attachToActivationSource_(cls, context):
        if context.activationSource:
            parentWindow = context.activationSource.window()
            if not parentWindow:
                return None
            glassWindow = cls.alloc().initWithParent_(parentWindow)
            context.glassWindows.add(glassWindow)
            return glassWindow
        else:
            return None
            
    def reset(self):
        self.setBackgroundColor_(NSColor.clearColor())
        self.setOpaque_(False)
        self.resetEventsMask()
    
    def canBecomeKeyWindow(self):
        return self._hijacksMouseInteraction # FIXME: hijacksKeyInteraction ?
        
    def resetEventsMask(self):
        # NSLeftMouseDown
        # NSLeftMouseUp
        # NSRightMouseDown
        # NSRightMouseUp
        # NSOtherMouseDown
        # NSOtherMouseUp
        # NSMouseMoved
        # NSLeftMouseDragged
        # NSRightMouseDragged
        # NSOtherMouseDragged
        # NSMouseEntered
        # NSMouseExited
        #self._handledEventsMask = NSLeftMouseUp|NSLeftMouseDown
        #self._hijacksMouseInteraction = False
        self.setAcceptsMouseMovedEvents_(True)
        
    def parentDidResize_(self, notification):
        print "Glasswindow parent did resize:", notification.object(), notification.object().frame()
        self.setFrame_display_(self.calcMyFrameFromParentFrame_(notification.object().frame()), True)
    
    def calcMyFrameFromParentFrame_(self, parentFrame):
        return parentFrame
        # return NSMakeRect(parentFrame.origin.x - 22, parentFrame.origin.y,
        #                           parentFrame.size.width + 22, parentFrame.size.height)
                          
    def setFrameView_(self, view):
        super(ScottyGlassWindow, self).setContentView_(view)
    
    def frameView(self):
        return super(ScottyGlassWindow, self).contentView()
        
    def scottyParentWindowWasReordered_relativeTo_(self, order, windowID):
        # We need this hack to make sure we receive an initial window ordering message when our
        # parent is made visible.  This hack relies on a category addition to NSWindows and a
        # swizzled-in overload to the NSWindow.orderWindow_relativeTo_ method that calls our
        # category method.
        #
        # This hack is necessary because our window appears not to receive mouse events until it
        # has received such an order message, even though the parent window takes over the ordering
        # of its child windows.  (Tested on OS X 10.5.8 and 10.6.0).
        if order != NSWindowOut:
            self.orderWindow_relativeTo_(NSWindowAbove, self.parentWindow().windowNumber())

    def setHijacksInteraction_(self, hijack):
        self._hijacksMouseInteraction = hijack
        self.setIgnoresMouseEvents_(not hijack)
        #self.resetEventsMask()
                
    def dealloc(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        Scotty().unregisterGlassWindow_(self)
        super(ScottyGlassWindow, self).dealloc()
        
GlassWindowModule.GlassWindow = ScottyGlassWindow
GlassWindow = ScottyGlassWindow

__all__ = 'GlassWindow ScottyGlassWindow'.split()