# TODO : refactor out of IIKit and into WILD

import IIKit

def extendIIKit(module):
    for attr in module.__all__:
        # print "adding", attr, "to IIKit"
        setattr(IIKit, attr, getattr(module, attr))

# Load WILD implementations
import WILDInstrumentManager; extendIIKit(WILDInstrumentManager)
import WILDSMEvents; extendIIKit(WILDSMEvents)

from IIKit import * # To support "from IIKit.wild import *"

del extendIIKit
del IIKit
