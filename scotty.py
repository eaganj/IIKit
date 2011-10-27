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

# TODO: Refactor out of IIKit and into Scotty

import IIKit

def extendIIKit(module):
    for attr in module.__all__:
        # print "adding", attr, "to IIKit"
        setattr(IIKit, attr, getattr(module, attr))

# Load Scotty versions
import ScottyInstrumentManager; extendIIKit(ScottyInstrumentManager)
import ScottyInstrumentContext; extendIIKit(ScottyInstrumentContext)
import ScottyGlassWindow; extendIIKit(ScottyGlassWindow)
import ScottyPickerInstrument; extendIIKit(ScottyPickerInstrument)
import ScottySMEvents; extendIIKit(ScottySMEvents)

from IIKit import * # To support "from IIKit.scotty import *"

del extendIIKit
del IIKit
