from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import os.path

import jre.cocoa

import InstrumentManager
from ScottyController import Scotty
from ScottyGlassWindow import GlassWindow

ModuleBundle = objc.currentBundle()

class ScottyInstrumentManager(InstrumentManager.InstrumentManager):
    def _loadInstrumentPlugins(self):
        from InstrumentLoader import InstrumentLoader
        searchDirs = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, 
                                            NSUserDomainMask|NSLocalDomainMask|NSNetworkDomainMask, True)
        appName = u"Scotty"
        searchDirs = [ os.path.join(baseDir, appName, u"Instruments") for baseDir in searchDirs ]
        searchDirs.append(os.path.join(ModuleBundle.builtInPlugInsPath(), u"Instruments"))
        InstrumentLoader.loadInstrumentsInSearchPaths(searchDirs)
        # for searchDir in searchDirs:
        #     # print "Searching in searchDir", searchDir
        #     if os.path.exists(searchDir):
        #         pluginPaths = [ os.path.join(searchDir, f) for f in os.listdir(searchDir) 
        #                                                                     if f.endswith(u'.instrument') ]
        #         for pluginPath in pluginPaths:
        #             try:
        #                 InstrumentLoader.loadInstrumentFromBundlePath(pluginPath)
        #             except Exception, e:
        #                 # FIXME: Should probably alert user
        #                 pluginName = os.path.basename(pluginPath)
        #                 NSLog(u"Could not load plugin: %s: %s: %s" % (pluginName, e.__class__.__name__, e))
    
    def glassViewForWindow(self, window):
        # FIXME: refactor into InstrumentManager instead of using Scotty
        glassWindow = Scotty().glassWindowForWindow_(window)
        if glassWindow:
            return glassWindow.contentView()
        else:
            return None
    
    def grabFullScreenGlassWindowForInstrument_(self, instrument):
        glassWindow = GlassWindow()
        Scotty().registerGlassWindow_(glassWindow)
        # glassWindow.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.0, 0.0, 0.05))
        glassWindow.setLevel_(NSStatusWindowLevel) #NSScreenSaverWindowLevel-100)
        glassWindow.orderFront_(None)
        return glassWindow
        
    def grabGlassWindowsForInstrument_hijackingInteraction_(self, instrument, hijack):
        return Scotty().grabGlassWindowsForInstrument_hijackingInteraction_(instrument, hijack)

    def ungrabGlassWindowsForInstrument_(self, instrument):
        Scotty().ungrabGlassWindowsForInstrument_(instrument)

InstrumentManager.InstrumentManager = ScottyInstrumentManager # Override InstrumentManager with Scotty version
InstrumentManager = ScottyInstrumentManager

__all__ = 'ScottyInstrumentManager InstrumentManager'.split()