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

from StateMachines import Event

def wrapEvent(event, instrument=None, namespace=None):
    # FIXME: Need to create a binding/mapping protocol for device events
    etype, device, name, value = event
    if instrument: # FIXME: this needs to be processed somewhere else.  Also, currently 0xDEADC0DE
        device = instrument.registeredDevices.get(device, device)
    
    # if (device, name) == ('Mouse', 'Point') or (device, name) == ('VICON', 'Position'):
    #     return PointEvent(*event)
    # elif (device, name) == ('Mouse', 'button1') or (device, name) == ('Button', 'Pressed'):
    #     return ButtonPressEvent(*event) if value and value[0] else ButtonReleaseEvent(*event)
    # else:
    #     return WILDEvent(*event)
    if (etype, name) == ('Pointing', 'Position'):
        return PointEvent(*event)
    elif (etype, name) == ('Toggling', 'Pressed'):
        return ButtonPressEvent(*event) if value and value[0] else ButtonReleaseEvent(*event)
    elif (etype, name) == ('Scotty', 'Pressed'):
        return ScottyPressEvent(*event) if value.pressed else ScottyReleaseEvent(*event)
    else:
        return WILDEvent(*event)

class WILDEvent(Event):
    def __init__(self, etype, device, name, value, namespace=None):
        super(WILDEvent, self).__init__(etype)
        self.device = device
        self.name = name
        self.value = value
    
    def match(self, transition):
        # First check if a device was specified in the transition
        if 'device' in transition.kwargs:
            return transition.kwargs['device'] == self.device
        else:
            return True
    
class PointEvent(WILDEvent):
    pass

class ButtonEvent(WILDEvent):
    pass

class ButtonPressEvent(ButtonEvent):
    pass

class ButtonReleaseEvent(ButtonEvent):
    pass

class ScottyPressEvent(WILDEvent):
    pass

class ScottyReleaseEvent(WILDEvent):
    pass


__eventMap = {
    ('Mouse', 'Point'): PointEvent,

}

__all__ = [ clsName for clsName, cls in locals().items() \
                if isinstance(cls, type) and issubclass(cls, WILDEvent) ]
