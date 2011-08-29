import re

strip_numbers_exp_str = r'\d+'
strip_numbers_exp = re.compile(strip_numbers_exp_str)

class IStarInstrumentContext(object):
    ''' InstrumentContexts are used to provide information about the environment in which an Instrument is
        being used.  They are currently only used in the Substance environment to create a binding between
        physical devices and instruments (such as binding a motion-tracked wand to a pointing instrument or
        a button on an iPad to an input event for a particular instrument).
        
        Normally, the state machine for an instrument is defined in terms of events and optionally logical
        devices.  This instrument context allows the mapping to be established between phyical devices and
        these logical devices.
    '''
    def __init__(self):
        ''' Initialization of contexts is parameterless.  Contexts are assumed to be empty unless individual
            parameters are specified.  Currently empty parameters include: 
                `cursor`: the cursor associated with the instrument, if any
                `activationSource`: (not used),
                `devices`: the list of physical devices available in the context,
                `boundDevices`: the list of physical devices that have been bound to a logical device, 
                `deviceLabels`: a dict from physical device name to label
        '''
        self.cursor = None
        self.activationSource = None
        self.devices = []
        self.boundDevices = set()
        self.deviceLabels = {} # Device labels, keyed by actual device
        self.glassWindows = {}

    def unboundDeviceFor(self, device_binding):
        ''' Request an unbound physical device for the specified `device_binding` request.  
            Returns the physical device if one is available in the context.  Otherwise, returns `None`.
            
            A `device_binding` request is a 2- or 3-tuple of the form:
                `(<logical device>, <allow_rebinding>, [<label>])` 
            where `allow rebinding` specifies whether exclusive control is needed over the physical device.
        '''
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
        ''' Establishes a binding from a logical device binding request to an instrument, if possible.
        
            FIXME: may silently fail if no physical device is available.
        '''
        actualDevice = self.unboundDeviceFor(logicalDevice)
        instrument.bindLogicalDeviceToActualDevice(logicalDevice, actualDevice)
        label = logicalDevice[2] if len(logicalDevice) > 2 else actualDevice.split('/')[-1]
        self.deviceLabels[actualDevice] = label
        return actualDevice, label

    def __str__(self):
        return '<%sInstrumentContext: %s>' % ('unbound ' if not self.cursor else '',
                                              self.cursor if self.cursor else '0x%s' % (id(self)))
    
    def attachGlassWindowToActivationSource(self, interactive=True):
        print "attachGlassWindowToActivationSource (stub)"
        pass

InstrumentContext = IStarInstrumentContext

__all__ = 'InstrumentContext'.split()