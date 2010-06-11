from AppKit import *
from Foundation import *
import objc

import jre.cocoa # To load NSEvent category additions

from IIKit import *
from StateMachines import *
from InstrumentManager import InstrumentManager

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
        
    def cocoaEvent(self):
        return self._cocoa_event
    
    # Cocoa General Event Info (See NSEvent API Ref)
    def context(self):
        return self._cocoa_event.context()
    
    def locationInWindow(self):
        return self._cocoa_event.locationInWindow()
    
    def locationInScreen(self):
        # This is not actually a part of Cocoa, but is present as a category addition in jre.cocoa.
        return self._cocoa_event.locationInScreen()

    def modifierFlags(self):
        return self._cocoa_event.modifierFlags()
    
    def timestamp(self):
        return self._cocoa_event.timestamp()
    
    def window(self):
        window = self._cocoa_event.window()
        if isinstance(window, (GlassWindow,)):
            return window.parentWindow()
        else:
            return window
            
    def cocoaWindow(self):
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

class CocoaActionEvent(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(CocoaActionEvent, self).__init__(args[0][0], sender=args[0][1], **options)
        else:
            super(CocoaActionEvent, self).__init__(self._senderMethodName, **options)

class MouseDown(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(MouseDown, self).__init__(args[0], **options)
        else:
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
    def __init__(self, *args, **options):
        if args:
            super(RightMouseDown, self).__init__(args[0], **options)
        else:
            super(RightMouseDown, self).__init__(NSRightMouseDown, **options)
    
# NSRightMouseUp
class RightMouseUp(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(RightMouseUp, self).__init__(args[0], **options)
        else:
            super(RightMouseUp, self).__init__(NSRightMouseUp, **options)
    
# NSMouseMoved
class MouseMoved(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(MouseMoved, self).__init__(args[0], **options)
        else:
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
    def __init__(self, *args, **options):
        if args:
            super(RightMouseDragged, self).__init__(args[0], **options)
        else:
            super(RightMouseDragged, self).__init__(NSRightMouseDragged, **options)

# NSMouseEntered
class MouseEntered(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(MouseEntered, self).__init__(args[0], **options)
        else:
            super(MouseEntered, self).__init__(NSMouseEntered, **options)
    
# NSMouseExited
class MouseExited(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(MouseExited, self).__init__(args[0], **options)
        else:
            super(MouseExited, self).__init__(NSMouseExited, **options)
    
# NSKeyDown
class KeyDown(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(KeyDown, self).__init__(args[0], **options)
        else:
            super(KeyDown, self).__init__(NSKeyDown, **options)
    
# NSKeyUp
class KeyUp(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(KeyUp, self).__init__(args[0], **options)
        else:
            super(KeyUp, self).__init__(NSKeyUp, **options)
    
# NSFlagsChanged
class FlagsChanged(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(FlagsChanged, self).__init__(args[0], **options)
        else:
            super(FlagsChanged, self).__init__(NSFlagsChanged, **options)
    
# NSAppKitDefined
class AppKitDefined(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(AppKitDefined, self).__init__(args[0], **options)
        else:
            super(AppKitDefined, self).__init__(NSAppKitDefined, **options)
    
# NSSystemDefined
class SystemDefined(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(SystemDefined, self).__init__(args[0], **options)
        else:
            super(SystemDefined, self).__init__(NSSystemDefined, **options)
    
# NSApplicationDefined 
class ApplicationDefined(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(ApplicationDefined, self).__init__(args[0], **options)
        else:
            super(ApplicationDefined, self).__init__(ApplicationDefined, **options)

# NSPeriodic
class Periodic(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(Periodic, self).__init__(args[0], **options)
        else:
            super(Periodic, self).__init__(NSPeriodic, **options)
    
# NSCursorUpdate
class CursorUpdate(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(CursorUpdate, self).__init__(args[0], **options)
        else:
            super(CursorUpdate, self).__init__(NSCursorUpdate, **options)
    
# NSScrollWheel
class ScrollWheel(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(ScrollWheel, self).__init__(args[0], **options)
        else:
            super(ScrollWheel, self).__init__(NSScrollWheel, **options)
    
# NSTabletPoint
class TabletPoint(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(TabletPoint, self).__init__(args[0], **options)
        else:
            super(TabletPoint, self).__init__(NSTabletPoint, **options)
    
# NSTabletProximity
class TabletProximity(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(TabletProximity, self).__init__(args[0], **options)
        else:
            super(TabletProximity, self).__init__(NSTabletProximity, **options)
    
# NSOtherMouseDown
class OtherMouseDown(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(OtherMouseDown, self).__init__(args[0], **options)
        else:
            super(OtherMouseDown, self).__init__(NSOtherMouseDown, **options)
    
# NSOtherMouseUp
class OtherMouseUp(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(OtherMouseUp, self).__init__(args[0], **options)
        else:
            super(OtherMouseUp, self).__init__(NSOtherMouseUp, **options)
    
# NSOtherMouseDragged
class OtherMouseDragged(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(OtherMouseDragged, self).__init__(args[0], **options)
        else:
            super(OtherMouseDragged, self).__init__(NSOtherMouseDragged, **options)

# NSEventTypeGesture
class EventTypeGesture(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeGesture, self).__init__(args[0], **options)
        else:
            super(EventTypeGesture, self).__init__(NSEventTypeGesture, **options)
    
# NSEventTypeMagnify
class EventTypeMagnify(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeMagnify, self).__init__(args[0], **options)
        else:
            super(EventTypeMagnify, self).__init__(NSEventTypeMagnify, **options)
    
# NSEventTypeSwipe
class EventTypeSwipe(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeSwipe, self).__init__(args[0], **options)
        else:
            super(EventTypeSwipe, self).__init__(NSEventTypeSwipe, **options)
    
# NSEventTypeRotate
class EventTypeRotate(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeRotate, self).__init__(args[0], **options)
        else:
            super(EventTypeRotate, self).__init__(NSEventTypeRotate, **options)
    
# NSEventTypeBeginGesture
class EventTypeBeginGesture(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeBeginGesture, self).__init__(args[0], **options)
        else:
            super(EventTypeBeginGesture, self).__init__(NSEventTypeBeginGesture, **options)

# NSEventTypeEndGesture
class EventTypeEndGesture(CocoaEvent):
    def __init__(self, *args, **options):
        if args:
            super(EventTypeEndGesture, self).__init__(args[0], **options)
        else:
            super(EventTypeEndGesture, self).__init__(NSEventTypeEndGesture, **options)

# Action method events
class CancelOperation(CocoaActionEvent):
    _senderMethodName = 'cancelOperation'

def cocoaEventWrapper(event):
    if isinstance(event, tuple):
        etype = event[0] # Unpack action method name
    else:
        etype = event.type()
    if etype in _eventMap:
        handlerName, eventClass = _eventMap[etype]
        return eventClass(event), handlerName
    else:
        return CocoaEvent(event), None

InstrumentManager.registerEventWrapper(cocoaEventWrapper, 'fr.lri.insitu.Scotty')
    
_eventMap = { 
                NSLeftMouseDown: ('mouseDown', LeftMouseDown),
                NSLeftMouseUp: ('mouseUp', LeftMouseUp),
                NSRightMouseDown: ('rightMouseDown', RightMouseDown),
                NSRightMouseUp: ('rightMouseUp', RightMouseUp),
                NSMouseMoved: ('mouseMoved', MouseMoved),
                NSLeftMouseDragged: ('mouseDragged', LeftMouseDragged),
                NSRightMouseDragged: ('rightMouseDragged', RightMouseDragged),
                NSMouseEntered: ('mouseEntered', MouseEntered),
                NSMouseExited: ('mouseExited', MouseExited),
                NSKeyDown: ('keyDown', KeyDown),
                NSKeyUp: ('keyUp', KeyUp),
                NSFlagsChanged: ('flagsChanged', FlagsChanged),
                NSAppKitDefined: ('appKitDefined', AppKitDefined),
                NSSystemDefined: ('systemDefined', SystemDefined),
                NSApplicationDefined: ('applicationDefined', ApplicationDefined),
                NSPeriodic: ('periodic', Periodic),
                NSCursorUpdate: ('cursorUpdate', CursorUpdate),
                NSScrollWheel: ('scrollWheel', ScrollWheel),
                NSTabletPoint: ('tabletPoint', TabletPoint),
                NSTabletProximity: ('tabletProximity', TabletProximity),
                NSOtherMouseDown: ('otherMouseDown', OtherMouseDown),
                NSOtherMouseUp: ('otherMouseUp', OtherMouseUp),
                NSOtherMouseDragged: ('otherMouseDragged', OtherMouseDragged),
                # TODO: (Gesture events)
                # NSEventTypeGesture   
                # NSEventTypeMagnify   
                # NSEventTypeSwipe     
                # NSEventTypeRotate    
                # NSEventTypeBeginGesture 
                # NSEventTypeEndGesture
                
                # Action methods
                'cancelOperation': ('cancelOperation', CancelOperation),
            }

__all__ = [ clsName for clsName, cls in locals().items() \
                if isinstance(cls, type) and issubclass(cls, CocoaEvent) ] + [ 'cocoaEventWrapper', ]