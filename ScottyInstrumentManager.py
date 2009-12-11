from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import os.path

import jre.cocoa

from InstrumentManager import *
from ScottyController import *

class ScottyInstrumentManager(InstrumentManager):
    def _loadInstrumentPlugins(self):
        from InstrumentLoader import InstrumentLoader
        searchDirs = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, 
                                            NSUserDomainMask|NSLocalDomainMask|NSNetworkDomainMask, True)
        appName = u"Scotty"
        searchDirs = [ os.path.join(baseDir, appName, u"Instruments") for baseDir in searchDirs ]
        searchDirs.append(os.path.join(objc.currentBundle().builtInPlugInsPath(), u"Instruments"))
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
                        NSLog(u"Could not load plugin: %s: %s: %s" % (pluginName, e.__class__.__name__, e))
        
    def grabGlassWindowsForInstrument_hijackingInteraction_(self, instrument, hijack):
        Scotty().grabGlassWindowsForInstrument_hijackingInteraction_(instrument, hijack)

    def ungrabGlassWindowsForInstrument_(self, instrument):
        Scotty().ungrabGlassWindowsForInstrument_hijackingInteraction_(instrument, hijack)

InstrumentManager = ScottyInstrumentManager

__all__ = 'ScottyInstrumentManager'.split()