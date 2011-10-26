# IIKit -- the Instrumental Interaction Toolkit
# Copyright 2009-2011, Université Paris-Sud
# by James R. Eagan (code at my last name dot me)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

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