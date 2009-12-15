from __future__ import with_statement

import jre.debug

from collections import deque

from InstrumentManager import *

class GlassWindow(object):
    def __init__(self, parent):
        pass # OVERRIDE IN SUBCLASSES
        
        self._hijacksMouseInteraction = False
    
    def resetEventsMask(self):
        pass # OVERRIDE IN SUBCLASSES
        
    def setHijacksInteraction_(self, hijack):
        self._hijacksMouseInteraction = hijack
        
    def mouseDown_(self, event):
        InstrumentManager.sharedInstrumentManager().mouseDown_(event)
    
    def mouseUp_(self, event):
        InstrumentManager.sharedInstrumentManager().mouseUp_(event)
    
    def mouseMoved_(self, event):
        pass # OVERRIDE IN SUBCLASSES
        
__all__ = 'GlassWindow'.split()