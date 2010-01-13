from __future__ import with_statement

import os.path

import jre.debug

import iStar

_sharedInstrumentManager = None

class IStarInstrumentManager(iStar.Object):
    def __init__(self):
        super(IStarInstrumentManager, self).__init__()
        
        self._instruments = {}
        self._activeInstrument = None
        self._glassViewsForInstrument = {}
    
    def init(self):
        self._loadInstrumentPlugins()
        
    @classmethod
    def sharedInstrumentManager(cls):
        global _sharedInstrumentManager
        
        if not _sharedInstrumentManager:
            _sharedInstrumentManager = cls()
            _sharedInstrumentManager.init()
        
        return _sharedInstrumentManager
    
    def _loadInstrumentPlugins(self):
        pass # OVERRIDE IN SUBCLASSES
    
    def addInstrument_(self, instrument):
        self._instruments[instrument.instrumentID] = instrument
    
    def removeInstrument_(self, instrument):
        del self._instruments[instrument.instrumentID]
    
    def instruments(self):
        return self._instruments.values()
    
    def instrumentWithID_(self, instrumentID):
        return self._instruments[instrumentID]
    
    def activateInstrument_(self, instrument):
        self._doActivateInstrument(instrument, instrument.activate)
    
    def activateInstrumentOnce_(self, instrument):
        self._doActivateInstrument_(instrument, instrument.activateOnce)
        
    def _doActivateInstrument_(self, instrument, activateMethod):
        self._activeInstrument = instrument
        activateMethod()
        self._glassViewsForInstrument[instrument.instrumentID] = set()
        if instrument.wantsGlassWindow():
            glassViews = self.grabGlassWindowsForInstrument_hijackingInteraction_(instrument,
                                                                     instrument.shouldHijackInteraction())
            self._glassViewsForInstrument[instrument.instrumentID].update(glassViews)
    
    def deactivateInstrument_(self, instrument):
        assert self._activeInstrument == instrument
        self._activeInstrument.deactivate()
        self._activeInstrument = None
        self.ungrabGlassWindowsForInstrument_(instrument)
    
    def activeInstrument(self):
        return self._activeInstrument    
    
    def mouseDown_(self, event):
        if hasattr(self._activeInstrument, 'mouseDown'):
            self._activeInstrument.mouseDown(event)
    
    def mouseUp_(self, event):
        if hasattr(self._activeInstrument, 'mouseUp'):
            self._activeInstrument.mouseUp(event)
    
    def mouseMoved_(self, event):
        if hasattr(self._activeInstrument, 'mouseMoved'):
            self._activeInstrument.mouseMoved(event)
    
    def glassViewForWindow(self, window):
        pass # OVERRIDE IN SUBCLASSES
    
    def grabGlassWindowsForInstrument_hijackingInteraction_(self, instrument, hijack):
        return [] # OVERRIDE IN SUBCLASSES

    def ungrabGlassWindowsForInstrument_(self, instrument):
        pass # OVERRIDE IN SUBCLASSES
    
    def resetGlassViewsForInstrument_(self, instrument):
        for glassView in self._glassViewsForInstrument[instrument.instrumentID]:
            if hasattr(glassView, 'reset'):
                glassView.reset()

InstrumentManager = IStarInstrumentManager

__all__ = 'InstrumentManager'.split()