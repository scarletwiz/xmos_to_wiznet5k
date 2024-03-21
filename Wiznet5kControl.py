from usocket import socket
from machine import Pin,SPI
import network
import time

class WIZNET5KControl():
    def __init__ (self, _spi, cs_pin=Pin(17), reset_pin=Pin(20)):
           
        self.nic = network.WIZNET5K(_spi, cs_pin,reset_pin) #spi,cs,reset pin
        self.nic.active(True)

    def set_network_info(self, net_info):
        self.nic.ifconfig(net_info)
        print('IP address :', self.nic.ifconfig())
        start_time = time.ticks_ms()
        
        while True:
            if self.nic.isconnected():
                return True
            else:
                time.sleep(1)
                
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            if elapsed_time > 3000:
                print("failed to network info setting up")
                return False

class WIZNET5K_Tcp():
    
    def __init__():
        self.sock = socket()

    def connect_to_server(self, addr, listen_cnt=1):
        self.sock.bind(addr)
        self.sock.listen(listen_cnt)
        
    def connect_to_client(self, dist_addr):
        self.sock.connect(dist_addr)
        
    def loopback_server(self):
        
    def loopback_client(self):

class WIZNET5K_Udp():
    def __init__ (self):
        self._sock= None
        
    def connect_to_udp(self, addr):
        self.udp_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind(addr)
        
    def loopback_udp(self):        



