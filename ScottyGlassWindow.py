from __future__ import with_statement

from AppKit import *
from Foundation import *
import objc

import jre.cocoa
import jre.debug

import GlassWindow as GlassWindowModule
from InstrumentManager import *
from ScottyController import Scotty

class ScottyGlassWindow(NSWindow, GlassWindowModule.GlassWindow):
    def __new__(cls, parent):
        return cls.alloc().initWithParent_(parent)
    
    def initWithParent_(self, parent):
        self = super(ScottyGlassWindow, self).initWithContentRect_styleMask_backing_defer_(
                                                parent.frame(),
                                                NSBorderlessWindowMask,
                                                NSBackingStoreBuffered,
                                                False
                                                )
        if not self:
            return self
        
        GlassWindowModule.GlassWindow.__init__(self, parent)
            
        self._hijacksMouseInteraction = False
        self.reset()
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                                                                           self,
                                                                           self.parentDidResize_,
                                                                           NSWindowDidResizeNotification,
                                                                           parent,
                                                                              )
        
        parent.addChildWindow_ordered_(self, NSWindowAbove)
        Scotty().registerGlassWindow_(self)
        
        # FIXME : refactor somewhere else
        #decoratorWindow = DecoratorWindow(parent)
        
        return self
    
    def reset(self):
        self.setBackgroundColor_(NSColor.clearColor())
        self.setOpaque_(False)
        self.resetEventsMask()
    
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
        
    def mouseDown_(self, event):
        #InstrumentManager.sharedInstrumentManager().mouseDown_(event)
        InstrumentManager.sharedInstrumentManager().handleEvent(event)
    
    def mouseUp_(self, event):
        #InstrumentManager.sharedInstrumentManager().mouseUp_(event)
        InstrumentManager.sharedInstrumentManager().handleEvent(event)
    
    def mouseDragged_(self, event):
        InstrumentManager.sharedInstrumentManager().handleEvent(event)
    
    def mouseMoved_(self, event):
        super(ScottyGlassWindow, self).mouseMoved_(event)
        
    def dealloc(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        Scotty().unregisterGlassWindow_(self)
        super(ScottyGlassWindow, self).dealloc()
        
GlassWindowModule.GlassWindow = ScottyGlassWindow
GlassWindow = ScottyGlassWindow

__all__ = 'GlassWindow ScottyGlassWindow'.split()