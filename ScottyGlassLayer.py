from AppKit import *
from Foundation import *
import objc

import jre.cocoa
import jre.debug

class ScottyGlassLayer(object):
    def __init__(self, parent):
        super(ScottyGlassLayer, self).__init__()
        
        if isinstance(parent, NSView):
            self.attachToView(parent)
        elif isinstance(parent, NSWindow):
            self.attachToWindow(parent)
        else:
            raise ValueError("Glass layer parent must be an NSView or NSWindow")
    
    def attachToView(self, view):
        # FIXME: Need to check if view is layer-hosting.  If yes, then just add our root layer as another layer.  If it's not layer-hosting, this approach should work.
        self._viewWantedLayer = view.wantsLayer()
        self._view = view
        self._auxView = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, *view.frame().size))
        
        # if view.wantsLayer():
        #     NSLog(u"Warning: attaching a ScottyGlassLayer to a layer-based view is untested. (%s in %s)" % (view, view.window().title() if view.window().title() else view.window()))
        #     self._rootLayer = view.layer()
        # else:
        #     self._rootLayer = CALayer.layer()
        #     view.setLayer_(self._rootLayer)
        #     view.setWantsLayer_(True)

        self._rootLayer = CALayer.layer()
        self._auxView.setLayer_(self._rootLayer)
        self._auxView.setWantsLayer_(True)
        view.addSubview_(self._auxView)
    
    def attachToWindow(self, window):
        self.attachToView(window.contentView())
    
    def detach(self):
        self._auxView.removeFromSuperview()
        self._auxView = None
        # if not self._viewWantedLayer:
        #     self._view.setWantsLayer_(False)
        #     self._view.setLayer_(None)
        
        # FIXME: TODO: remove all added layers
    
    def addLayer(self, layer):
        layer.setFrame_(NSMakeRect(0, 0, *self._rootLayer.frame().size))
        self._rootLayer.addSublayer_(layer)
    
    def removeLayer(self, layer):
        # TODO
        pass

GlassLayer = ScottyGlassLayer

__all__ = 'ScottyGlassLayer GlassLayer'.split()