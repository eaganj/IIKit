from __future__ import with_statement

import jre.debug

from collections import deque

from InstrumentManager import *
import iStar

# TODO:  Make GlassWindow itself an instrument
class IStarGlassWindow(iStar.Object):
    def __init__(self, parent):
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