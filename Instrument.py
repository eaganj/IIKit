# -*- coding: utf-8 -*-
#
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

import copy
import imp
import os
import sys
import warnings

import jre.debug

from InstrumentManager import *

import Object

class Instrument(Object.Object):
    _bundleID = None
    _bundle_ = None
    instrumentID = None
    name = None
    verb = None
    consumesEvents = True
    priority = 0
    
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
        
    def activate(self, context=None):
        self._active = True
        self._context = context
    
    def activateOnce(self, context=None):
        self._activatedOnce = True
        self.activate(context)
    
    def deactivate(self):
        if self._active or self._activatedOnce:
            self._active = self._activatedOnce = False
            self._context = None
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