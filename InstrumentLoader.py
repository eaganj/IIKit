from __future__ import with_statement

### TODO:  Implement pure-Python bundle loading
from Foundation import *
from AppKit import *
import objc

import copy
import imp
import os
import sys
import warnings

import jre.cocoa
import jre.debug

from InstrumentManager import *
from Instrument import *
import iStar

class InstrumentLoader(iStar.Object):
    currentBundle = None
    
    @classmethod
    @jre.debug.trap_exceptions
    def loadInstrumentFromBundlePath(cls, bundlePath):
        bundle = NSBundle.bundleWithPath_(bundlePath)
        cls.currentBundle = bundle
        try:
            bundleID = bundle.bundleIdentifier()
            bundleInfo = bundle.infoDictionary()
            scriptName = 'iStar.' + bundleID
            scriptPath = bundle.pathForResource_ofType_(bundleInfo['iStarInstrumentScriptName'], None)
            if not scriptPath:
                raise Exception('Could not find instrument code (%s)' % \
                                            (bundleInfo['iStarInstrumentScriptName']))
            scriptFileName = os.path.basename(scriptPath)
    
            module = cls._loadScript(scriptName, scriptPath)
            globalEnvItems = set(globals().keys())
            instruments = set()
            for name, value in module.__dict__.iteritems():
                # if name not in globalEnvItems and hasattr(value, '__module__'):
                #     print 'Checking', name, 'defined in', value.__module__
        
                # Check if defined in the loaded module and a valid Instrument class
                if (getattr(value, '__module__', None) == scriptName 
                    or name in getattr(module, '__all__', [])) \
                   and isinstance(value, type) and issubclass(value, Instrument):
                    # instrument matches all required criteria ; all systems are go
                    instruments.add(value)
    
            instrumentManager = InstrumentManager.sharedInstrumentManager()
            for instrumentClass in instruments:
                instrumentID = u'%s/%s' % (bundleID, instrumentClass.__name__)
                #print 'Adding instrument', instrumentID
                instrument = instrumentClass(instrumentID)
                instrument._bundle_ = bundle
                instrumentManager.addInstrument_(instrument)
        finally:
            cls.currentBundle = None

    @classmethod
    def _loadScript(cls, name, path):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Parent module '.*' not found")
            try:
                oldPath = copy.copy(sys.path)
                sys.path.append(os.path.dirname(path))
                module = imp.load_source(name, path)
                return module
            finally:
                sys.path = oldPath
            # Alternative method: use runpy.run_module
    
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