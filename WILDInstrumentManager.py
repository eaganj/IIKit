import InstrumentManager
import WILDEvents as events
import iStarWrapper

class WILDInstrumentManager(iStarWrapper.Object, InstrumentManager.InstrumentManager):
    def handleEvent(self, event, namespace):
        print "event:", namespace, event
        instrument = self._activeInstrument
        
        if instrument.stateMachine:
            wildEvent = events.wrapEvent(event)
            instrument.stateMachine.process_event(wildEvent)
    
    def _loadInstrumentPlugins(self):
        from WILDInstrumentLoader import InstrumentLoader
        searchDirs = [ u'~/Library/Application Support/WILD Instruments',
                       u'~/.WILD Instruments',
                       u'/Library/Application Support/WILD Instruments',
                       u'/usr/local/share/wild/instruments',
                       u'/usr/share/wild/instruments',
                       u'/Network/Library/Application Support/WILD Instruments',
                     ]
        searchDirs = [ os.path.expanduser(searchDir) for searchDir in searchDirs ]
        for searchDir in searchDirs:
            # print "Searching in searchDir", searchDir
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

InstrumentManager.InstrumentManager = WILDInstrumentManager # Override InstrumentManager with WILD version
InstrumentManager = WILDInstrumentManager

__all__ = 'InstrumentManager WILDInstrumentManager'.split()