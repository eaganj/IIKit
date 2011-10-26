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

import InstrumentManager as InstrumentManagerModule
from InstrumentManager import IStarInstrumentManager

import os
import sys

import jre.debug

from substance.core.bootstrap import *
from substance.std.tools.oobridge import OOAccessor


class SubstanceInstrumentManager(Facet, IStarInstrumentManager):
    """The Substance Instrument Manager"""
    
    # @Facet.DEPENDENCY("VICON", "The place where the VICON 2D Input representation is stored and updated")
    # @Facet.DEPENDENCY("OSC", "The place where the OSC Input controller facet resides")
    @Facet.DEPENDENCY("Scene Graph", "The Scene Graph of the WILD Universe")
    def __init__(self):
        # super(SubstanceInstrumentManager, self).__init__("InstrumentManager")
        Facet.__init__(self, "InstrumentManager")
        IStarInstrumentManager.__init__(self)
        
        self.__installedNode = None
        self.__instrumentCounter = 0
        
    def instantiate(self, with_state):
        assert self.__installedNode is None, "SubstanceInstrumentManager has already been instantiated"
        self.__installedNode = self.node
        self._sg = local.get_dependency(self, "Scene Graph")
        
        
        assert not self._sg.has_facet(self, "OOAccessor")
        self._ooaccessor = OOAccessor()
        self._sg.add_facet(self, self._ooaccessor, True, True)
        
        print "Instrument Manager loaded and installed on", self.__installedNode
        
        # if self._instruments:
        #     instrument = self._instruments.get('fr.lri.eaganj.instrument.Mover/MoveInstrument',
        #                                        self._instruments.values()[0])
        #     local.InstrumentManager.activateInstrument_(self, instrument)
        
        
        # self.vicon = local.get_dependency(self, "VICON")
        # self.osc = local.get_dependency(self, "OSC")

    def _loadInstrumentPlugins(self):
        from InstrumentLoader import InstrumentLoader
        searchDirs = [ u'~/Library/Application Support/Substance Instruments',
                       u'~/.substance/instruments',
                       u'/Library/Application Support/Substance Instruments',
                       u'/usr/local/share/substance/instruments',
                       u'/usr/share/substance/instruments',
                       u'/Network/Library/Application Support/Substance Instruments',
                     ]
        searchDirs = [ os.path.expanduser(searchDir) for searchDir in searchDirs ]
        InstrumentLoader.loadInstrumentsInSearchPaths(searchDirs)


    @Facet.HANDLER("<void>::<void>")
    def handleEvent(self, rawEvent, namespace):
        return super(SubstanceInstrumentManager, self).handleEvent(rawEvent, namespace)
        
    @Facet.HANDLER("<void::void>")
    @jre.debug.trap_exceptions
    def activateInstrument(self, instrumentOrInstrumentClass, context):
        self.__instrumentCounter += 1
        instrumentNodeName = "Instrument %s" % (self.__instrumentCounter)
        self.instrumentNode = local.new_child(self, instrumentNodeName, 
                                              instrumentOrInstrumentClass.instrumentID)
        self.instrumentNode.set_dependency(self, "Scene Graph", self._sg, "The Scene Graph")
        
        instrument = super(SubstanceInstrumentManager, self).activateInstrument_(
                                                                    instrumentOrInstrumentClass)
        self._prepareInstrumentContext(instrument, context)
        instrument.ooaccessor = self._ooaccessor
        
        # print ">>> Activated instrument", instrument.instrumentID
        return instrument
    
    def _prepareInstrumentContext(self, instrument, context):
        for logical_device in instrument.getDevices():
            physical_device, label = context.bindLogicalDeviceToInstrument(logical_device, instrument)
            # print "---    ", logical_device, "->", physical_device, "(%s)" % (label)
    
    def _instantiateInstrument(self, instrumentClass):
        instrument = instrumentClass()
        self.instrumentNode.add_facet(self, instrument, True, True)
        return instrument
    
    def sortedInstruments(self):
        # FIXME: Improve to properly use a priority queue/stack
        result = []
        for instrument in self._instruments.values():
            if instrument.priority == 1:
                result.insert(0, instrument)
            else:
                result.append(instrument)
        
        return result
        
    def _sortedActiveInstruments(self):
        # FIXME: Improve to properly use a priority queue/stack
        result = []
        for instrument in self._activeInstruments:
            if instrument.priority == 1:
                result.insert(0, instrument)
            else:
                result.append(instrument)
        
        return result
        

InstrumentManagerModule.InstrumentManager = SubstanceInstrumentManager
InstrumentManager = SubstanceInstrumentManager

__all__ = 'SubstanceInstrumentManager InstrumentManager'.split()