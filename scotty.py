# TODO: Refactor out of IIKit and into Scotty

import IIKit

def extendIIKit(module):
    for attr in module.__all__:
        # print "adding", attr, "to IIKit"
        setattr(IIKit, attr, getattr(module, attr))

# Load Scotty versions
import ScottyInstrumentManager; extendIIKit(ScottyInstrumentManager)
import ScottyGlassWindow; extendIIKit(ScottyGlassWindow)
import ScottyPickerInstrument; extendIIKit(ScottyPickerInstrument)
import ScottySMEvents; extendIIKit(ScottySMEvents)

from IIKit import * # To support "from IIKit.scotty import *"

del extendIIKit
del IIKit
