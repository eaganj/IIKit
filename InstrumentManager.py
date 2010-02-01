from __future__ import with_statement

import os.path

import jre.debug

import iStar

_sharedInstrumentManager = None

class IStarInstrumentManager(iStar.Object):
    def __init__(self):
        super(IStarInstrumentManager, self).__init__()
        
        self._instruments = {}
        self._devices = []
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
    
    # @classmethod
    # def WILDInstrumentManager(cls, iibridge, node):
    #     # FIXME : refactor this
    #     # TODO: add a proper WILDInstrumentManager with a sceneGraph attr
    #     import WILDInstrumentManager
    #     return WILDInstrumentManager.WILDInstrumentManager(iibridge, node)
        
    
    def _loadInstrumentPlugins(self):
        pass # OVERRIDE IN SUBCLASSES
    
    def addInstrument_(self, instrument):
        self._instruments[instrument.instrumentID] = instrument
    
    def removeInstrument_(self, instrument):
        del self._instruments[instrument.instrumentID]
    
    def addDevice(self, device):
        self._devices.append(device)
    
    def removeDevice(self, device):
        self._devices.remove(device)
    
    def deviceChanged(self, device):
        pass #FIXME
    
    def instruments(self):
        return self._instruments.values()
    
    def instrumentWithID_(self, instrumentID):
        return self._instruments[instrumentID]
    
    def activateInstrument_(self, instrument):
        self._doActivateInstrument_(instrument, instrument.activate)
    
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
    
    @jre.debug.trap_exceptions
    def handleEvent(self, event):
        instrument = self._activeInstrument
        
        if instrument.stateMachine:
            print "Passing event to stateMachine"
            eventWrapper = self._eventMap[event.type()][1]
            instrument.stateMachine.process_event(eventWrapper(event))
        else:
            eventHandlerMethod = getattr(instrument, self._eventMap[event.type()][0], None)
            print "event type", event.type(), "to", eventHandlerMethod
            if eventHandlerMethod:
                eventHandlerMethod(event)
    
    def mouseDown_(self, event):
        if hasattr(self._activeInstrument, 'mouseDown'):
            self._activeInstrument.mouseDown(event)
    
    def mouseUp_(self, event):
        if hasattr(self._activeInstrument, 'mouseUp'):
            self._activeInstrument.mouseUp(event)
    
    def mouseMoved_(self, event):
        if hasattr(self._activeInstrument, 'mouseMoved'):
            self._activeInstrument.mouseMoved(event)
    
    def mouseDragged_(self, event):
        if hasattr(self._activeInstrument, 'mouseDragged'):
            self._activeInstrument.mouseDragged(event)
    
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
    
    _eventMap = { } # OVERRIDE IN SUBCLASSES

InstrumentManager = IStarInstrumentManager

__all__ = 'InstrumentManager'.split()