import ixf86config
import exceptions


def readConfigFile(*args):
    return apply(ixf86config.readConfigFile, args)

def addComment(*args):
    return apply(ixf86config.addComment, args)

def XF86SupportedDepths():
    return (8, 16, 24)
#    return (8, 15, 16, 24)

def XF86SupportedResolutions():
    return [ "640x480", "800x480", "800x512", "800x600", "1024x600", "1024x768",
             "1152x768", "1152x864", "1280x800", "1280x960",
             "1280x1024", "1400x1050", "1440x900", "1600x1024", "1600x1200",
             "1680x1050", "1900x1200", "1920x1200", "1920x1440", "2048x1536"]

def XF86Option(name = None, val = None):
    o = ixf86config.XF86Option()
    o.name = name
    o.val = val
    return o

def XF86ConfFiles():
    return ixf86config.XF86ConfFiles()

def XF86ConfModule():
    return ixf86config.XF86ConfModule()

def XF86ConfLoad(name = None):
    l = ixf86config.XF86ConfLoad()
    l.name = name
    return l

def XF86ConfFlags():
    return ixf86config.XF86ConfFlags()

def XF86ConfVideoPort():
    return ixf86config.XF86ConfVideoPort()

def XF86ConfVideoAdaptor():
    return ixf86config.XF86ConfVideoAdaptor()

def XF86ConfModeLine():
    return ixf86config.XF86ConfModeLine()

def XF86ConfModes():
    return ixf86config.XF86ConfModes()

def XF86ConfModesLink():
    return ixf86config.XF86ConfModesLink()

def XF86ConfMonitor():
    return ixf86config.XF86ConfMonitor()

def XF86ConfInput():
    return ixf86config.XF86ConfInput()

def XF86ConfDevice():
    dev = ixf86config.XF86ConfDevice()
    dev.chipid = -1
    dev.chiprev = -1
    dev.irq = -1
    return dev

def XF86ConfAdaptorLink():
    return ixf86config.XF86ConfAdaptorLink()

def XF86Mode(name):
    mode = ixf86config.XF86Mode()
    if name != None:
        mode.name = name
    return mode

def XF86ConfDisplay():
    display = ixf86config.XF86ConfDisplay()
    #unset the white and black fields by default
    display.white = (-1,-1,-1)
    display.black = (-1,-1,-1)
    return display

def XF86ConfScreen():
    # ROCKS
    screen = ixf86config.XF86ConfScreen()
    screen.options.insert(XF86Option("SecurityTypes", "None"))
    screen.options.insert(XF86Option("localhost", "1"))
    # return ixf86config.XF86ConfScreen()
    return screen
    # ROCKS

def XF86ConfAdjacency():
    return ixf86config.XF86ConfAdjacency()

def XF86ConfInactive():
    return ixf86config.XF86ConfInactive()

def XF86ConfInputref(device = None, option = None):
    ref = ixf86config.XF86ConfInputref()
    if device != None:
        ref.inputdev = device
    if option != None:
        ref.options.insert(XF86Option (option))
    return ref

def XF86ConfLayout():
    return ixf86config.XF86ConfLayout()

def XF86ConfBuffers():
    return ixf86config.XF86ConfBuffers()

def XF86ConfDRI():
    return ixf86config.XF86ConfDRI()

def XF86ConfVendSub():
    return ixf86config.XF86ConfVendSub()

def XF86ConfVendor():
    return ixf86config.XF86ConfVendor()

def XF86Config():
    return ixf86config.XF86Config()

class XF86SectionMissing(exceptions.Exception):
    def __init__(self,msg):
        self.msg = msg

def lookupDevice(xconfig, device_id):
    if device_id is None:
        raise XF86SectionMissing("Empty device identifier given")

    for d in xconfig.device:
        if (d.identifier == device_id):
            return d
    raise XF86SectionMissing("No device found with the identifier" + device_id)

def lookupMonitor(xconfig, monitor_id):
    if monitor_id is None:
        raise XF86SectionMissing("Empty monitor identifier given")

    for m in xconfig.monitor:
        if m.identifier == monitor_id:
            return m
    raise XF86SectionMissing("No monitor found with the identifier" + monitor_id)
    
def lookupScreen(xconfig, screen_id):
    if screen_id is None:
        raise XF86SectionMissing("Empty screen identifier given")

    for s in xconfig.screen:
        if (s.identifier == screen_id):
            return s
    raise XF86SectionMissing("No screen found with the identifier" + screen_id)
    
def lookupInputDevice(xconfig, input_id):
    if input_id is None:
        raise XF86SectionMissing("Empty input identifier given")

    for i in xconfig.input:
        if (i.identifier == input_id):
            return i
    raise XF86SectionMissing("No input device found with the identifier" + input_id)
    
def getCorePointer(xconfig):
    for i in xconfig.layout[0].inputs:
        for o in i.options:
            if o.name == "CorePointer":
                return lookupInputDevice(xconfig, i.inputdev) 
    raise XF86SectionMissing("No CorePointer InputDevice found in the layout")
 
def getCoreKeyboard(xconfig):
    for i in xconfig.layout[0].inputs:
        for o in i.options:
            if o.name == "CoreKeyboard":
                return lookupInputDevice(xconfig, i.inputdev) 
    raise XF86SectionMissing("No CoreKeyboard InputDevice found in the layout")
 
def getPrimaryScreen(xconfig):
    try:
        screen_id = xconfig.layout[0].adjacencies[0].screen
    except IndexError, e:
        raise XF86SectionMissing("No primary Screen found in the layout")
    return  lookupScreen(xconfig, screen_id)

def getAllScreens(xconfig):
    screen_list = []

    try:
        for i in xconfig.layout[0].adjacencies:
            screen_list.append(lookupScreen(xconfig, i.screen))
    except IndexError, e:
        raise XF86SectionMissing("No screens found in the layout")
    return  screen_list
        
def createTemplate():
    def setupLayout(layout):
        layout.identifier = "Default Layout"
        layout.adjacencies.insert(XF86ConfAdjacency())
        layout.adjacencies[0].screen = "Screen0"
        layout.inputs.insert (XF86ConfInputref ("Keyboard0", "CoreKeyboard"))

    def setupKeyboard(keyboard):
        keyboard.comment = ""
        keyboard.identifier = "Keyboard0"
        keyboard.driver = "kbd"
        keyboard.options.insert (XF86Option("XkbModel", "pc101"))
        keyboard.options.insert (XF86Option("XkbLayout", "us"))

    def setupVideocard(device):
        device.identifier = "Videocard0"
        device.driver = "svga"

    def setupScreen(screen):
        screen.identifier = "Screen0"
        screen.device = "Videocard0"
        screen.defaultdepth = 24

    xconfig = XF86Config()
    
    xconfig.comment = "# Xorg configuration created by pyxf86config\n"

    xconfig.layout.insert(XF86ConfLayout())
    setupLayout(xconfig.layout[0])

    xconfig.modules = XF86ConfModule()

    # ROCKS
    xconfig.modules.load.insert(XF86ConfLoad("vnc"))
    # ROCKS

    keyboard = XF86ConfInput()
    xconfig.input.insert(keyboard)
    setupKeyboard(keyboard)

    device = XF86ConfDevice()
    xconfig.device.insert(device)
    setupVideocard(device)

    screen = XF86ConfScreen()
    xconfig.screen.insert(screen)
    setupScreen(screen)

    return xconfig
