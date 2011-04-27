from __future__ import with_statement

import jre.debug

from collections import deque

from InstrumentManager import *
import iStar

# TODO:  Make GlassWindow itself an instrument
class IStarGlassWindow(iStar.Object):
    ''' A glass window is a transparent overlay that can be attached to an existing object, such as a widget,
        window, or the full screen.  It acts as a child of this object, following it as its position updates.
        Glass windows are useful for drawing annotations on top of an existing widget or even replacing its 
        appearance entirely.  They can also optionally intercept and redirect input events, transforming the
        behavior of the parent object.
        
        FIXME:  The GlassWindow interface is currently in transition.
    '''
    def __init__(self, parent=None):
        ''' Create a new glass window attached to `parent`.  If no parent is provided, then a fulllscreen
            glass window is created instead.
        '''
        super(IStarGlassWindow, self).__init__()
        pass # OVERRIDE IN SUBCLASSES
        
        self._hijacksMouseInteraction = False
    
    def resetEventsMask(self):
        pass # OVERRIDE IN SUBCLASSES
        
    def setHijacksInteraction_(self, hijack):
        self._hijacksMouseInteraction = hijack
    
    def reset(self):
        pass # OVERRIDE IN SUBCLASSES
        
GlassWindow = IStarGlassWindow
        
__all__ = 'GlassWindow'.split()