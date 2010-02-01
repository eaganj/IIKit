from AppKit import *
from Foundation import *
import objc

from StateMachines import *

import copy

# Event Types as of OS 10.6.2
    # NSLeftMouseDown     
    # NSLeftMouseUp       
    # NSRightMouseDown    
    # NSRightMouseUp      
    # NSMouseMoved        
    # NSLeftMouseDragged  
    # NSRightMouseDragged 
    # NSMouseEntered      
    # NSMouseExited       
    # NSKeyDown            
    # NSKeyUp              
    # NSFlagsChanged       
    # NSAppKitDefined      
    # NSSystemDefined      
    # NSApplicationDefined 
    # NSPeriodic           
    # NSCursorUpdate       
    # NSScrollWheel        
    # NSTabletPoint        
    # NSTabletProximity    
    # NSOtherMouseDown     
    # NSOtherMouseUp       
    # NSOtherMouseDragged 
    # NSEventTypeGesture   
    # NSEventTypeMagnify   
    # NSEventTypeSwipe     
    # NSEventTypeRotate    
    # NSEventTypeBeginGesture 
    # NSEventTypeEndGesture


class CocoaEvent(Event):
    def __init__(self, etype, *args, **options):
        if isinstance(etype, NSEvent):
            self._cocoa_event = etype
            etype = etype.type()
        else:
            etype = etype
        super(CocoaEvent, self).__init__(etype)
        
        self.options = copy.copy(options)
    
    def __match__(self, transition):
        assert isinstance(self.type, NSEvent), "Event does not wrap a Cocoa Event"
        for option, value in self.options.items():
            if hasattr(self.type, option):
                if getattr(self.type, option) != value:
                    return False
        
        return True
    
    # Cocoa General Event Info (See NSEvent API Ref)
    def context(self):
        return self._cocoa_event.context()
    
    def locationInWindow(self):
        return self._cocoa_event.locationInWindow()
    
    def modifierFlags(self):
        return self._cocoa_event.modifierFlags()
    
    def timestamp(self):
        return self._cocoa_event.timestamp()
    
    def window(self):
        # FIXME: check if event is really delivered to a glass window !
        window = self._cocoa_event.window()
        if not window:
            return window
        else:
            return window.parentWindow()
    
    def glassWindow(self):
        return self._cocoa_event.window() # FIXME: check if event is really delivered to a glass window !
    
    def windowNumber(self):
        return self._cocoa_event.windowNumber()
    
    def eventRef(self):
        return self._cocoa_event.eventRef()
    
    def CGEvent(self):
        return self._cocoa_event.CGEvent()
    
    # Cocoa Key Event Info (See NSEvent API Ref)
    def characters(self):
        return self._cocoa_event.characters()
    
    def charactersIgnoringModifiers(self):
        return self._cocoa_event.charactersIgnoringModifiers()
    
    def isARepeat(self):
        return self._cocoa_event.isARepeat()
    
    def keyCode(self):
        return self._cocoa_event.keyCode()
    
    # Cocoa Mouse Event Info (See NSEvent API Ref)
    def buttonNumber(self):
        return self._cocoa_event.buttonNumber()
    
    def clickCount(self):
        return self._cocoa_event.clickCount()
    
    def pressure(self):
        return self._cocoa_event.pressure()
    
    # TODO:  Other Cocoa Event info (See NSEvent API Ref)

class MouseDown(CocoaEvent):
    def __init__(self, **options):
        super(MouseDown, self).__init__(NSMouseEvent, **options)

# NSLeftMouseDown
class LeftMouseDown(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(LeftMouseDown, self).__init__(args[0], **options)
        else:
            super(LeftMouseDown, self).__init__(NSLeftMouseDown, **options)
    
# NSLeftMouseUp
class LeftMouseUp(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(LeftMouseUp, self).__init__(args[0], **options)
        else:
            super(LeftMouseUp, self).__init__(NSLeftMouseUp, **options)
    
# NSRightMouseDown
class RightMouseDown(CocoaEvent):
    def __init__(self, **options):
        super(RightMouseDown, self).__init__(NSRightMouseDown, **options)
    
# NSRightMouseUp
class RightMouseUp(CocoaEvent):
    def __init__(self, **options):
        super(RightMouseUp, self).__init__(NSRightMouseUp, **options)
    
# NSMouseMoved
class MouseMoved(CocoaEvent):
    def __init__(self, **options):
        super(MouseMoved, self).__init__(NSMouseMoved, **options)
    
# NSLeftMouseDragged
class LeftMouseDragged(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(LeftMouseDragged, self).__init__(args[0], **options)
        else:
            super(LeftMouseDragged, self).__init__(NSLeftMouseDragged, **options)
    
# NSRightMouseDragged 
class RightMouseDragged(CocoaEvent):
    def __init__(self, **options):
        super(RightMouseDragged, self).__init__(NSRightMouseDragged, **options)

# NSMouseEntered
class MouseEntered(CocoaEvent):
    def __init__(self, **options):
        super(MouseEntered, self).__init__(NSMouseEntered, **options)
    
# NSMouseExited
class MouseExited(CocoaEvent):
    def __init__(self, **options):
        super(MouseExited, self).__init__(NSMouseExited, **options)
    
# NSKeyDown
class KeyDown(CocoaEvent):
    def __init__(self, **options):
        super(KeyDown, self).__init__(NSKeyDown, **options)
    
# NSKeyUp
class KeyUp(CocoaEvent):
    def __init__(self, **options):
        super(KeyUp, self).__init__(NSKeyUp, **options)
    
# NSFlagsChanged
class FlagsChanged(CocoaEvent):
    def __init__(self, **options):
        super(FlagsChanged, self).__init__(NSFlagsChanged, **options)
    
# NSAppKitDefined
class AppKitDefined(CocoaEvent):
    def __init__(self, **options):
        super(AppKitDefined, self).__init__(NSAppKitDefined, **options)
    
# NSSystemDefined
class SystemDefined(CocoaEvent):
    def __init__(self, **options):
        super(SystemDefined, self).__init__(NSSystemDefined, **options)
    
# NSApplicationDefined 
class ApplicationDefined(CocoaEvent):
    def __init__(self, **options):
        super(ApplicationDefined, self).__init__(ApplicationDefined, **options)

# NSPeriodic
class Periodic(CocoaEvent):
    def __init__(self, **options):
        super(Periodic, self).__init__(NSPeriodic, **options)
    
# NSCursorUpdate
class CursorUpdate(CocoaEvent):
    def __init__(self, **options):
        super(CursorUpdate, self).__init__(NSCursorUpdate, **options)
    
# NSScrollWheel
class ScrollWheel(CocoaEvent):
    def __init__(self, **options):
        super(ScrollWheel, self).__init__(NSScrollWheel, **options)
    
# NSTabletPoint
class TabletPoint(CocoaEvent):
    def __init__(self, **options):
        super(TabletPoint, self).__init__(NSTabletPoint, **options)
    
# NSTabletProximity
class TabletProximity(CocoaEvent):
    def __init__(self, **options):
        super(TabletProximity, self).__init__(NSTabletProximity, **options)
    
# NSOtherMouseDown
class OtherMouseDown(CocoaEvent):
    def __init__(self, **options):
        super(OtherMouseDown, self).__init__(NSOtherMouseDown, **options)
    
# NSOtherMouseUp
class OtherMouseUp(CocoaEvent):
    def __init__(self, **options):
        super(OtherMouseUp, self).__init__(NSOtherMouseUp, **options)
    
# NSOtherMouseDragged
class OtherMouseDragged(CocoaEvent):
    def __init__(self, **options):
        super(OtherMouseDragged, self).__init__(NSOtherMouseDragged, **options)

# NSEventTypeGesture
class EventTypeGesture(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeGesture, self).__init__(NSEventTypeGesture, **options)
    
# NSEventTypeMagnify
class EventTypeMagnify(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeMagnify, self).__init__(NSEventTypeMagnify, **options)
    
# NSEventTypeSwipe
class EventTypeSwipe(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeSwipe, self).__init__(NSEventTypeSwipe, **options)
    
# NSEventTypeRotate
class EventTypeRotate(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeRotate, self).__init__(NSEventTypeRotate, **options)
    
# NSEventTypeBeginGesture
class EventTypeBeginGesture(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeBeginGesture, self).__init__(NSEventTypeBeginGesture, **options)

# NSEventTypeEndGesture
class EventTypeEndGesture(CocoaEvent):
    def __init__(self, **options):
        super(EventTypeEndGesture, self).__init__(NSEventTypeEndGesture, **options)
    
__all__ = [ clsName for clsName, cls in locals().items() \
                if isinstance(cls, type) and issubclass(cls, CocoaEvent) ]