import network
import XmosControl
import Wiznet5kControl
from machine import Pin,UART,SPI

def main ():

    net_info= ('192.168.11.20','255.255.255.0','192.168.11.1','8.8.8.8')
    
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18)) #pico spi configure
    w5k = Wiznet5kControl.WIZNET5KControl(spi)
    w5k.set_network_info(net_info)
    w5k.connect_to_client(('192.168.11.100', 5000))
    
    uart=UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    xmos = XmosControl.RecvDataFromXmos(uart, keepAlive=False)
    
    while True:
        data= xmos.command_uart_from_xmos_parsing()
        if data:
            w5k.cli_sock.send(data)
            print(">> send data is: ", data)
            

if __name__ == "__main__":
    main()