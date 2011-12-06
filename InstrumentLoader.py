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

from __future__ import with_statement

from collections import deque
import copy
import imp
import os
import sys
import warnings

import jre.debug
from jre.util.bundle import Bundle

from InstrumentManager import *
from Instrument import *
from StateMachines.translator import *
import Object


class InstrumentLoader(Object.Object):
    ''' The Instrument Loader is responsible for deserializing instrument plugins stored on disk.
    '''
    currentBundle = None
    
    @classmethod
    def loadInstrumentsInSearchPaths(cls, searchDirs):
        pluginPaths = []
        for searchDir in searchDirs:
            print "Searching in searchDir", searchDir
            if os.path.exists(searchDir):
                pluginPaths.extend([ os.path.join(searchDir, f) for f in os.listdir(searchDir) 
                                                                      if f.endswith(u'.instrument') ])
                        
        if not pluginPaths:
            return # Nothing to load
            
        pluginBundles = [ Bundle.bundleWithPath_(path) for path in pluginPaths ]
        pluginBundles = cls.sortPluginBundles(pluginBundles)
        
        for pluginBundle in pluginBundles:
            try:
                cls.loadInstrumentFromBundle(pluginBundle)
            except Exception, e:
                # FIXME: Should probably alert user
                pluginName = os.path.basename(pluginBundle.bundlePath())
                NSLog(u"Could not load plugin: %s: %s: %s" % (pluginName, e.__class__.__name__, e))
    
    @classmethod
    def sortPluginBundles(cls, bundles):
        handles = [ (bundle.bundleIdentifier(), bundle) for bundle in bundles ]
        bundleWithID = dict(handles)
        parentsForID = dict([ (bundle.bundleIdentifier(), bundle.infoDictionary().get('IIKit Required Plugins', [])) for bundle in bundles ])
        
        visited = set()
        def visit(node, result):
            if node in visited:
                return
                
            for parent in parentsForID[node]:
                visit(parent, result)
                visited.add(parent)
                result.append(parent)
            result.append(node)
        
        result = []
        for bundleID in bundleWithID:
            visit(bundleID, result)
        return [ bundleWithID[bundleID] for bundleID in result ]
    
    @classmethod
    def loadInstrumentFromBundlePath(cls, bundlePath):
        cls.loadInstrumentFromBundle(Bundle.bundleWithPath_(bundlePath))
        
    @classmethod
    @jre.debug.trap_exceptions
    def loadInstrumentFromBundle(cls, bundle):
        cls.currentBundle = bundle
        try:
            bundleID = bundle.bundleIdentifier()
            bundleInfo = bundle.infoDictionary()
            scriptName = 'IIKit.plugin.' + bundleID
            scriptPath = bundle.pathForResource_ofType_(bundleInfo['IIKitInstrumentScriptName'], None)
            if not scriptPath:
                raise Exception('Could not find instrument code (%s)' % \
                                            (bundleInfo['IIKitInstrumentScriptName']))
            scriptFileName = os.path.basename(scriptPath)
            moduleName = os.path.splitext(os.path.basename(scriptPath))[0]
            moduleFullName = '%s.%s' % (scriptName, moduleName)
    
            module = cls._loadScript(scriptName, scriptPath)
            globalEnvItems = set(globals().keys())
            instruments = set()
            
            for name, value in module.__dict__.iteritems():
                # if name not in globalEnvItems and hasattr(value, '__module__'):
                #     print 'Checking', name, 'defined in', value.__module__
        
                # Check if defined in the loaded module and a valid Instrument class
                if (getattr(value, '__module__', None) == moduleFullName 
                    or name in getattr(module, '__all__', [])) \
                   and isinstance(value, type) and issubclass(value, Instrument):
                    # instrument matches all required criteria ; all systems are go
                    instruments.add(value)
    
            instrumentManager = InstrumentManager.sharedInstrumentManager()
            for instrumentClass in instruments:
                instrumentID = u'%s/%s' % (bundleID, instrumentClass.__name__)
                # print 'Adding instrument', instrumentID
                instrumentClass.registerInstrument(instrumentID, bundle)
                instrumentManager.addInstrument_(instrumentClass)
        finally:
            cls.currentBundle = None


    @classmethod
    def _loadScript(cls, name, path):
        if path.endswith('.pysm'):
            cls._translatePySM(path)
            path = path[:-2]
            
        with warnings.catch_warnings():
            parentName = name[:name.rfind('.')]
            parentModule = cls._createParentModule(name, path)
            moduleName = os.path.splitext(os.path.basename(path))[0]
            moduleFullName = '%s.%s' % (name, moduleName)
            try:
                oldPath = copy.copy(sys.path)
                sys.path.insert(0, os.path.dirname(path))
                if os.path.exists(path + 'c') and \
                    (not os.path.exists(path) or os.stat(path + 'c').st_mtime >= os.stat(path).st_mtime):
                    module = imp.load_compiled(moduleFullName, path + 'c')
                else:
                    module = imp.load_source(moduleFullName, path)

                module.__bundle__ = cls.currentBundle
                return module
            finally:
                sys.path = oldPath
            
            # Alternative method: use runpy.run_module
    
    @classmethod
    def _createParentModule(cls, name, path):
        fullPath = 'IIKit'
        for part in name.split('.')[1:]:
            fullPath = '.'.join([fullPath, part])
            if fullPath not in sys.modules:
                new_module = imp.new_module(fullPath)
                new_module.__file__ = "<stub>"
                new_module.__package__ = []
                sys.modules[fullPath] = new_module
    
    @classmethod
    def _translatePySM(cls, path):
        PySMTranslator().translate(path, path[:-2])
    
        
    
# Make sure we have a catch_warnings context manager (introduced in Python 2.6)
try:
    from warnings import catch_warnings
except ImportError:
    ### Code ripped from Python 2.6 source tree
    class catch_warnings(object):

        """A context manager that copies and restores the warnings filter upon
        exiting the context.

        The 'record' argument specifies whether warnings should be captured by a
        custom implementation of warnings.showwarning() and be appended to a list
        returned by the context manager. Otherwise None is returned by the context
        manager. The objects appended to the list are arguments whose attributes
        mirror the arguments to showwarning().

        The 'module' argument is to specify an alternative module to the module
        named 'warnings' and imported under that name. This argument is only useful
        when testing the warnings module itself.

        """

        def __init__(self, record=False, module=None):
            """Specify whether to record warnings and if an alternative module
            should be used other than sys.modules['warnings'].

            For compatibility with Python 3.0, please consider all arguments to be
            keyword-only.

            """
            self._record = record
            self._module = sys.modules['warnings'] if module is None else module
            self._entered = False
    
        def __repr__(self):
            args = []
            if self._record:
                args.append("record=True")
            if self._module is not sys.modules['warnings']:
                args.append("module=%r" % self._module)
            name = type(self).__name__
            return "%s(%s)" % (name, ", ".join(args))

        def __enter__(self):
            if self._entered:
                raise RuntimeError("Cannot enter %r twice" % self)
            self._entered = True
            self._filters = self._module.filters
            self._module.filters = self._filters[:]
            self._showwarning = self._module.showwarning
            if self._record:
                log = []
                def showwarning(*args, **kwargs):
                    log.append(WarningMessage(*args, **kwargs))
                self._module.showwarning = showwarning
                return log
            else:
                return None

        def __exit__(self, *exc_info):
            if not self._entered:
                raise RuntimeError("Cannot exit %r without entering first" % self)
            self._module.filters = self._filters
            self._module.showwarning = self._showwarning
    
    # warnings is already imported at the top of this module
    warnings.catch_warnings = catch_warnings

__all__ = 'InstrumentLoader'.split()
