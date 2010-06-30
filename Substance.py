# Unlike most other IIKit bootstrap entry points, this file is uppercased to avoid a conflict with the "substance" package on which it relies.

# TODO : refactor out of IIKit and into WILD

import IIKit

def extendIIKit(module):
    for attr in module.__all__:
        # print "adding", attr, "to IIKit"
        setattr(IIKit, attr, getattr(module, attr))

# Load Substance implementations
import SubstanceInstrument; extendIIKit(SubstanceInstrument)
import SubstanceInstrumentManager; extendIIKit(SubstanceInstrumentManager)
import SubstanceSMEvents; extendIIKit(SubstanceSMEvents)
import InstrumentContext; extendIIKit(InstrumentContext)

from IIKit import * # To support "from IIKit.wild import *"

del extendIIKit
del IIKit
