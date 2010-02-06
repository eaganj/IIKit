import copy
import imp
import os
import sys
import warnings

import jre.debug

from InstrumentManager import *

import iStar

class Instrument(iStar.Object):
    _bundleID = None
    _bundle_ = None
    instrumentID = None
    name = None
    verb = None
    
    @classmethod
    def registerInstrument(cls, instrumentID, bundle=None):
        cls.instrumentID = instrumentID
        cls._bundle_ = bundle
        if bundle:
            cls._bundleID = bundle.bundleIdentifier()
    
    def __init__(self):
        super(Instrument, self).__init__()        
        self._active = False
        self._activatedOnce = False
        
        self.action = None
        self.target = None
        
        self.stateMachine = None
        self.registeredDevices = {} # Used to map physical devices to logical names
        
        #self._bundle_ = None
    
    def isActive(self):
        return self._active
    active = property(isActive)
        
    def activate(self):
        self._active = True
    
    def activateOnce(self):
        self._activatedOnce = True
        self.activate()
    
    def deactivate(self):
        if self._active or self._activatedOnce:
            self._active = self._activatedOnce = False
            InstrumentManager.sharedInstrumentManager().deactivateInstrument_(self)
    
    def performActionOn(self, obj):
        # FIXME: implement action/protocol interface!
        if self.action:
            self.action(obj)
        
        if self._activatedOnce:
            self.deactivate()
    
    def shouldHijackInteraction(self):
        return False
    
    def wantsGlassWindow(self):
        return self.shouldHijackInteraction()
    
    def newGlassViewForWindow(self, window):
        '''
        Create and return a new view suitable for use as the `contentView` of a `GlassWindow` when this
        instrument is the current active instrument.  This method will be called to create a new
        `GlassView` for each `NSWindow` in the current application.
        
        Instruments that provide visual feedback should use this method to setup their drawing environment.
        
        By default, this method returns `None` to use an empty `NSView`
        '''
        return None
        
__all__ = 'Instrument'.split()