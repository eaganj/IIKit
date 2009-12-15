
try:
    import Foundation
    import AppKit
    import objc    
except ImportError:
    # PyObjC not found -- ignore and don't try loading Cocoa extensions
    from Instrument import *
    from InstrumentLoader import *
    from InstrumentManager import *
    from GlassWindow import *
    from PickerInstrument import *
else:
    # Load Scotty versions
    from Instrument import *
    from InstrumentLoader import *
    from ScottyInstrumentManager import *
    from ScottyGlassWindow import *
    from ScottyPickerInstrument import *