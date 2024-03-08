import network
import XmosControl
from machine import Pin,UART

def main ():

    uart=UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

    xmos=XmosControl.RecvDataFromXmos(uart)

    while True:
        data= xmos.command_uart_from_xmos_parsing()
        if data:
            print(">> send data is: ", data)

if __name__ == "__main__":
    main()