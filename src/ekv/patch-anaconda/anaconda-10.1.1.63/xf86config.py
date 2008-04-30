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
    return [  "640x480",   "800x480",   "800x600",  "1024x600", "1024x768",
	     "1152x768",  "1152x864",  "1280x800",  "1280x960",
            "1280x1024", "1400x1050",  "1440x900", "1600x1200",
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
    return ixf86config.XF86ConfScreen()

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
    for d in xconfig.device:
        if (d.identifier == device_id):
            return d
    raise XF86SectionMissing("No device found with the identifier" + device_id)

def lookupMonitor(xconfig, monitor_id):
    for m in xconfig.monitor:
        if m.identifier == monitor_id:
            return m
    raise XF86SectionMissing("No monitor found with the identifier" + monitor_id)
    
def lookupScreen(xconfig, screen_id):
    for s in xconfig.screen:
        if (s.identifier == screen_id):
            return s
    raise XF86SectionMissing("No screen found with the identifier" + screen_id)
    
def lookupInputDevice(xconfig, input_id):
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
    def setupFiles(files):
        files.comment = \
        "# RgbPath is the location of the RGB database.  Note, this is the name of the \n" + \
        "# file minus the extension (like \".txt\" or \".db\").  There is normally\n" + \
        "# no need to change the default.\n\n" + \
        "# Multiple FontPath entries are allowed (they are concatenated together)\n" + \
        "# By default, Red Hat 6.0 and later now use a font server independent of\n" + \
        "# the X server to render fonts.\n\n"

        files.rgbpath = "/usr/X11R6/lib/X11/rgb"
        files.fontpath = "unix/:7100"

    def setupLayout(layout):
        layout.identifier = "Default Layout"
        layout.adjacencies.insert(XF86ConfAdjacency())
        layout.adjacencies[0].screen = "Screen0"
        layout.inputs.insert (XF86ConfInputref ("Mouse0", "CorePointer"))
        layout.inputs.insert (XF86ConfInputref ("Keyboard0", "CoreKeyboard"))
      
    def setupModules(modules):
        modules.load.insert (XF86ConfLoad ("dbe"))
        modules.load.insert (XF86ConfLoad ("extmod"))
        modules.load.insert (XF86ConfLoad ("fbdevhw"))
        modules.load.insert (XF86ConfLoad ("glx"))
        modules.load.insert (XF86ConfLoad ("record"))
        modules.load.insert (XF86ConfLoad ("freetype"))
        modules.load.insert (XF86ConfLoad ("type1"))

        #
        # SDSC
        #
        modules.load.insert (XF86ConfLoad ("vnc"))
        #
        # SDSC
        #
       
    def setupKeyboard(keyboard):
        keyboard.comment = \
"""# Specify which keyboard LEDs can be user-controlled (eg, with xset(1))
#	Option	"Xleds"		"1 2 3"

# To disable the XKEYBOARD extension, uncomment XkbDisable.
#	Option	"XkbDisable"

# To customise the XKB settings to suit your keyboard, modify the
# lines below (which are the defaults).  For example, for a non-U.S.
# keyboard, you will probably want to use:
#	Option	"XkbModel"	"pc102"
# If you have a US Microsoft Natural keyboard, you can use:
#	Option	"XkbModel"	"microsoft"
#
# Then to change the language, change the Layout setting.
# For example, a german layout can be obtained with:
#	Option	"XkbLayout"	"de"
# or:
#	Option	"XkbLayout"	"de"
#	Option	"XkbVariant"	"nodeadkeys"
#
# If you'd like to switch the positions of your capslock and
# control keys, use:
#	Option	"XkbOptions"	"ctrl:swapcaps"
# Or if you just want both to be control, use:
#	Option	"XkbOptions"	"ctrl:nocaps"
#
"""
        keyboard.identifier = "Keyboard0"
        keyboard.driver = "kbd"
#        keyboard.options.insert (XF86Option("XkbRules", "xorg"))
        keyboard.options.insert (XF86Option("XkbModel", "pc101"))
        keyboard.options.insert (XF86Option("XkbLayout", "us"))
        
    def setupMouse(mouse):
        mouse.identifier = "Mouse0"
        mouse.driver = "mouse"
        mouse.options.insert (XF86Option("Protocol", "IMPS/2"))
        mouse.options.insert (XF86Option("Device", "/dev/input/mice"))
        mouse.options.insert (XF86Option("ZAxisMapping", "4 5"))
        mouse.options.insert (XF86Option("Emulate3Buttons", "no"))

    def setupMonitor(monitor):
        monitor.identifier = "Monitor0"
        monitor.vendor = "Monitor Vendor"
        monitor.modelname = "Monitor Model"
        #Generic Extended Super VGA, 800x600 @ 60 Hz, 640x480 @ 72 Hz; 0; 31.5-37.9; 50-70
        monitor.n_hsync = 1
        monitor.hsync[0] = (31.5, 37.9)
        monitor.n_vrefresh = 1
        monitor.vrefresh[0] = (50.0, 70.0)
        monitor.options.insert (XF86Option("dpms"))

    def setupVideocard(device):
        device.identifier = "Videocard0"
        device.vendor = "Videocard vendor"
        device.board = "Videocard"
        device.driver = "svga"

    def setupScreen(screen):
        screen.identifier = "Screen0"
        screen.device = "Videocard0"
        screen.monitor = "Monitor0"
        screen.defaultdepth = 16

        #
        # SDSC
        #
        screen.options.insert (XF86Option("SecurityTypes", "None"))
        screen.options.insert (XF86Option("localhost", "1"))
        #
        # SDSC
        #

    xconfig = XF86Config()
    
    xconfig.comment = "# XFree86 4 configuration created by pyxf86config\n"

    xconfig.files = XF86ConfFiles()
    setupFiles (xconfig.files)

    xconfig.layout.insert(XF86ConfLayout())
    setupLayout(xconfig.layout[0])

    xconfig.modules = XF86ConfModule()
    setupModules(xconfig.modules)

    keyboard = XF86ConfInput()
    xconfig.input.insert(keyboard)
    setupKeyboard(keyboard)

    mouse = XF86ConfInput()
    xconfig.input.insert(mouse)
    setupMouse(mouse)

    monitor = XF86ConfMonitor()
    xconfig.monitor.insert(monitor)
    setupMonitor(monitor)

    device = XF86ConfDevice()
    xconfig.device.insert(device)
    setupVideocard(device)

    screen = XF86ConfScreen()
    xconfig.screen.insert(screen)
    setupScreen(screen)

    dri = XF86ConfDRI()
    xconfig.dri = dri
    dri.mode = 0666

    return xconfig
    
