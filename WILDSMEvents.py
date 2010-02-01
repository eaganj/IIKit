from StateMachines import Event

def wrapEvent(event, namespace=None):
    # FIXME: Need to create a binding/mapping protocol for device events
    etype, device, name, value = event
    
    if (device, name) == ('Mouse', 'Point'):
        return PointEvent(event)
    elif (device, name) == ('Button', 'Pressed'):
        return ButtonPressEvent(event) if value else ButtonReleaseEvent(event)
    else:
        return WILDEvent(event)

class WILDEvent(Event):
    def __init__(self, etype, device, name, value, namespace=None):
        super(WILDEvent, self).__init__(etype)
        self.device = device
        self.name = name
        self.value = value
    
class PointEvent(WILDEvent):
    pass

class ButtonEvent(WILDEvent):
    pass

class ButtonPressEvent(ButtonEvent):
    pass

class ButtonReleaseEvent(ButtonEvent):
    pass


__eventMap = {
    ('Mouse', 'Point'): PointEvent,

}