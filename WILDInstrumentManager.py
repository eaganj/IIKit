import InstrumentManager
# import WILDEvents as events # TODO
import iStarWrapper

class WILDInstrumentManager(iStarWrapper.Object, InstrumentManager.InstrumentManager):
    pass
    
    def handleEvent(self, event, namespace):
        print "event:", namespace, event
    
    # def _loadInstrumentPlugins(self):
    #     from InstrumentLoader import InstrumentLoader
    #     searchDirs = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, 
    #                                         NSUserDomainMask|NSLocalDomainMask|NSNetworkDomainMask, True)
    #     appName = u"Scotty"
    #     searchDirs = [ os.path.join(baseDir, appName, u"Instruments") for baseDir in searchDirs ]
    #     searchDirs.append(os.path.join(ModuleBundle.builtInPlugInsPath(), u"Instruments"))
    #     for searchDir in searchDirs:
    #         # print "Searching in searchDir", searchDir
    #         if os.path.exists(searchDir):
    #             pluginPaths = [ os.path.join(searchDir, f) for f in os.listdir(searchDir) 
    #                                                                         if f.endswith(u'.instrument') ]
    #             for pluginPath in pluginPaths:
    #                 try:
    #                     InstrumentLoader.loadInstrumentFromBundlePath(pluginPath)
    #                 except Exception, e:
    #                     # FIXME: Should probably alert user
    #                     pluginName = os.path.basename(pluginPath)
    #                     NSLog(u"Could not load plugin: %s: %s: %s" % (pluginName, e.__class__.__name__, e))