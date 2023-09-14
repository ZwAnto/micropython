import neopixel
from machine import Pin
from time import sleep
from network import STA_IF, WLAN

class UserInterrupt(Exception):
    pass

def singleton(cls):
    instance = None
    def getinstance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return getinstance

@singleton
class Led:
    __colormap = {
        'red': (1,0,0),
        'green': (0,1,0),
        'blue': (0,0,1),
        'orange': (3,1,0),
        'pink': (3,0,1),
        'purple': (1,0,1),
        'cyan': (0,1,1)
    }
    def __init__(self):
        self.np = neopixel.NeoPixel(Pin(2), 1)
        
    def set(self, color):
        if isinstance(color, tuple):
            self.np[0] = color
        elif isinstance(color, str):
            self.np[0] = self.__colormap[color]
        self.np.write()
        
    def off(self):
        self.np[0] = (0,0,0)
        self.np.write()
        
@singleton
class Wifi:
    def __init__(self, ssid, password, ifconfig):
        
        
        self.ssid = ssid
        self.password = password
        self.ifconfig = ifconfig
        
        self.network = None
        self.isnetworksetup = False
    
    @property
    def isconnected(self):
        if self.network:
            return self.network.isconnected()
        else:
            return False
        
    def _init_network(self):
        self.network = WLAN(STA_IF)
        self.network.ifconfig(self.ifconfig)
        self.isnetworksetup = True
        
    def connect(self):
        Led().set('purple')
        print("Connecting to " + self.ssid)
        
        if not self.isconnected:
                
            if not self.isnetworksetup:
                self._init_network()
                
            self.network.active(False)
            self.network.active(True)
            self.network.connect(self.ssid, self.password)
            
        counter = 0
        while not self.network.isconnected():
            sleep(1)
            counter = counter + 1
            if counter > 15:
                counter = 0
                self._init__connection()
                
        Led().off()
        
    def disconnect(self):
        print("Disconnecting from " + self.ssid)
        self.network.disconnect()
        self.network.active(False)
        
    def __enter__(self):
        self.connect()

    def __exit__(self, *args, **kwargs):
        self.disconnect()




