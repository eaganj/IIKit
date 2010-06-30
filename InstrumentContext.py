import re

strip_numbers_exp_str = r'\d+'
strip_numbers_exp = re.compile(strip_numbers_exp_str)

class InstrumentContext(object):
    def __init__(self):
        self.cursor = None
        self.devices = []
        self.boundDevices = set()
        self.deviceLabels = {} # Device labels, keyed by actual device

    def unboundDeviceFor(self, device_binding):
        # print "unboundDeviceFor:", device_binding
        if not device_binding:
            return None
        if len(device_binding) > 2:
            device, allow_rebinding, label = device_binding
        else:
            device, allow_rebinding = device_binding
        pattern = strip_numbers_exp.sub('', device.split('/')[-1])
        # print "Searching for", pattern, "devices"
        to_bind = None
        for unbound in self.devices:
            if strip_numbers_exp.sub('', unbound.split('/')[-1]) == pattern:
                to_bind = unbound
                break
        
        if to_bind:
            if not allow_rebinding:
                self.devices.remove(to_bind)
            self.boundDevices.add(to_bind)
        
        return to_bind
    
    def bindLogicalDeviceToInstrument(self, logicalDevice, instrument):
        actualDevice = self.unboundDeviceFor(logicalDevice)
        instrument.bindLogicalDeviceToActualDevice(logicalDevice, actualDevice)
        label = logicalDevice[2] if len(logicalDevice) > 2 else actualDevice.split('/')[-1]
        self.deviceLabels[actualDevice] = label
        return actualDevice, label

    def __str__(self):
        return '<%sInstrumentContext: %s>' % ('unbound ' if not self.cursor else '',
                                              self.cursor if self.cursor else '0x%s' % (id(self)))

__all__ = 'InstrumentContext'.split()