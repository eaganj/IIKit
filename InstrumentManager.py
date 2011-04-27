from __future__ import with_statement

import inspect
import os.path

import jre.debug

import iStar

_sharedInstrumentManager = None
_eventWrappers = { }

class IStarInstrumentManager(iStar.Object):
    def __init__(self):
        super(IStarInstrumentManager, self).__init__()
        
        self._instruments = {}
        self._devices = []
        # self._activeInstrument = None
        self._activeInstruments = []
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
    
    def addDevice(self, device):
        self._devices.append(device)
    
    def removeDevice(self, device):
        self._devices.remove(device)
    
    def deviceChanged(self, device):
        pass #FIXME
    
    def instruments(self):
        return self._instruments.values()
    
    def sortedInstruments(self):
        return sorted(self._instruments.values())
    
    def instrumentWithID_(self, instrumentID):
        return self._instruments[instrumentID]
    
    def _sortedActiveInstruments(self):
        return reversed(self._activeInstruments)
        
    def activateInstrument_(self, instrument):
        return self.activateInstrument_withContext_once_(instrument, None, False)
        # return self._doActivateInstrument_(instrument, instrument.activate)
    
    def activateInstrumentOnce_(self, instrument):
        return self.activateInstrument_withContext_once_(instrument, None, True)
        # return self._doActivateInstrument_(instrument, instrument.activateOnce)
    
    def activateInstrument_withContext_once_(self, instrument, context, once):
        activateMethod = instrument.activateOnce if once else instrument.activate
        return self._doActivateInstrument_withContext_(instrument, context, activateMethod)
        
    def _doActivateInstrument_(self, instrumentOrInstrumentClass, activateMethod):
        return self._doActivateInstrument_withContext_(instrumentOrInstrumentClass, 
                                                       context, activateMethod)

    def _doActivateInstrument_withContext_(self, instrumentOrInstrumentClass, context, activateMethod):
        if inspect.isclass(instrumentOrInstrumentClass):
            instrument = self._instantiateInstrument(instrumentOrInstrumentClass)
            self._activeInstrument = instrument
            self._activeInstruments.append(instrument)
            instrument.instrumentManager = self
            activateMethod(instrument, context)
        else:
            instrument = instrumentOrInstrumentClass
            self._activeInstrument = instrument
            self._activeInstruments.append(instrument)
            instrument.instrumentManager = self
            activateMethod(context)
        
        self._glassViewsForInstrument[instrument.instrumentID] = set()
        if instrument.wantsGlassWindow():
            glassViews = self.grabGlassWindowsForInstrument_hijackingInteraction_(instrument,
                                                                     instrument.shouldHijackInteraction())
            self._glassViewsForInstrument[instrument.instrumentID].update(glassViews)
        
        return instrument
    
    def _instantiateInstrument(self, instrumentClass):
        return instrumentClass()
        
    def deactivateInstrument_(self, instrument):
        # assert self._activeInstrument == instrument
        self._activeInstrument.deactivate()
        self._activeInstrument = None
        self._activeInstruments.remove(instrument)
        instrument.instrumentManager = None
        self.ungrabGlassWindowsForInstrument_(instrument)
        
    @classmethod
    def registerEventWrapper(cls, wrapper, namespace):
        assert namespace not in _eventWrappers, "Handler already registered for namespace"
        _eventWrappers[namespace] = wrapper
        
    @jre.debug.trap_exceptions
    def handleEvent(self, rawEvent, namespace):
        event, handlerMethodName = self.wrapEvent(rawEvent, namespace)
        # print "handleEvent:", event, handlerMethodName
        # for instrument in reversed(self._activeInstruments):
        for instrument in self._sortedActiveInstruments():
            # print "Delivering event", event, "to", instrument.instrumentID
            if instrument.stateMachine:
                handled = instrument.stateMachine.process_event(event)
                if handled and instrument.consumesEvents:
                    return True
            elif handlerMethodName:
                handlerMethod = getattr(instrument, handlerMethodName, None)
                if handlerMethod:
                    handlerMethod(event)
                    return True
        
        return False
    
    def wrapEvent(self, event, namespace):
        return _eventWrappers[namespace](event)
    
    def glassViewForWindow(self, window):
        pass # OVERRIDE IN SUBCLASSES
    
    def grabGlassWindowsForInstrument_hijackingInteraction_(self, instrument, hijack):
        return [] # OVERRIDE IN SUBCLASSES

    def ungrabGlassWindowsForInstrument_(self, instrument):
        pass # OVERRIDE IN SUBCLASSES
    
    def grabFullScreenGlassWindowForInstrument_(self, instrument):
        pass # OVERRIDE IN SUBCLASSES
    
    def resetGlassViewsForInstrument_(self, instrument):
        for glassView in self._glassViewsForInstrument[instrument.instrumentID]:
            if hasattr(glassView, 'reset'):
                glassView.reset()
    

InstrumentManager = IStarInstrumentManager

__all__ = 'InstrumentManager'.split()