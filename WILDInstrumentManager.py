import InstrumentManager
import WILDSMEvents as events
import iStarWrapper

import os
import pdb
import sys

InstrumentManagerModule = sys.modules['IIKit.InstrumentManager']

import jre.debug

class WILDInstrumentManager(iStarWrapper.Object, InstrumentManager.InstrumentManager):
    def register(self, sceneGraph):
        ### FIXME: This is an ugly hack to support bootstrapping into the H-Graph
        assert InstrumentManagerModule._sharedInstrumentManager is None, \
               "Shared InstrumentManager already exists"
        InstrumentManagerModule._sharedInstrumentManager = self
        
        self.sceneGraph = sceneGraph
        self.init()
        print "WILD Instrument manager successfully registered"
        
    @jre.debug.trap_exceptions
    def handleEvent(self, event, namespace):
        # print "event:", namespace, event
        instrument = self._activeInstrument
        
        if instrument and instrument.stateMachine:
            #pdb.set_trace()
            wildEvent = events.wrapEvent(event, instrument=instrument)
            instrument.stateMachine.process_event(wildEvent)
    
    def _loadInstrumentPlugins(self):
        from WILDInstrumentLoader import InstrumentLoader
        searchDirs = [ u'~/Library/Application Support/WILD Instruments',
                       u'~/.wild/instruments',
                       u'/Library/Application Support/WILD Instruments',
                       u'/usr/local/share/wild/instruments',
                       u'/usr/share/wild/instruments',
                       u'/Network/Library/Application Support/WILD Instruments',
                     ]
        searchDirs = [ os.path.expanduser(searchDir) for searchDir in searchDirs ]
        for searchDir in searchDirs:
            print "Searching in searchDir", searchDir
            if os.path.exists(searchDir):
                pluginPaths = [ os.path.join(searchDir, f) for f in os.listdir(searchDir) 
                                                                            if f.endswith(u'.instrument') ]
                for pluginPath in pluginPaths:
                    try:
                        InstrumentLoader.loadInstrumentFromBundlePath(pluginPath)
                    except Exception, e:
                        # FIXME: Should probably alert user
                        pluginName = os.path.basename(pluginPath)
                        print u"Could not load plugin: %s: %s: %s" % (pluginName, e.__class__.__name__, e)
        
        # FIXME: create instrument selection interface
        if self._instruments:
            instrument = self._instruments.get('fr.lri.eaganj.instrument.Mover/MoveInstrument',
                                               self._instruments.values()[0])
            self.activateInstrument_(instrument)
    
    def _doActivateInstrument_(self, instrument, activateMethod):
        instrument.registeredDevices = { 'VICON': 'pointer', }
        instrument.sceneGraph = self.sceneGraph
        super(WILDInstrumentManager, self)._doActivateInstrument_(instrument, activateMethod)
    
    # def _doActivateInstrument_(self, instrument, activateMethod):
    #     curriedActivateMethod = lambda instrumentID: activateMethod(instrumentID, self.sceneGraph)
    #     super(WILDInstrumentManager, self)._doActivateInstrument_(instrument, curriedActivateMethod)

# InstrumentManager.InstrumentManager = WILDInstrumentManager # Override InstrumentManager with WILD version
InstrumentManager = WILDInstrumentManager

__all__ = 'InstrumentManager WILDInstrumentManager'.split()
