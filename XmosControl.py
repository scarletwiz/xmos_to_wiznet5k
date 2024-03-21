import time
import json

from machine import UART

class RecvDataFromXmos:

    def __init__(self, uart, keepAlive=True):
        self._uart = uart
        
        self.xmos_active = False
        self.last_status_msg_time = time.ticks_ms()
        self.last_send_time = time.ticks_ms()
        
    def set_xmos_status_active(self):
        if self.xmos_active == False:
            self.xmos_active=True
        self.last_status_msg_time= time.ticks_ms()
        
    def set_xmos_status_inactive(self):
        if self.xmos_active == False:
            return
        self.xmos_active=False
        self.last_status_msg_time= None

    def check_xmos_status_timeout(self):
        current_time = time.ticks_ms()

        if self.xmos_active and time.ticks_diff(current_time, self.last_status_msg_time) > 5000:  # 5초 이상 '.' 수신 없음
            print("No '.' received for 5 seconds. Status changed to False.")
            self.set_xmos_status_inactive()
            
        if time.ticks_diff(current_time, self.last_send_time) > 1000:            
            self.last_send_time = current_time
            data = {
                "command": "None",
                "id": 0,
                "xmos_status": self.xmos_active
            }
            return json.dumps(data)
        return None

    def command_check_device_start(self, msg, timeout_duration=5000):
        start_msg = b'App build at'
        #end_msg = b'\\xff\\xff\\x7f\\xf8\\xff\\xe0'
        end_msg= b'\r\n\r\n'

        if start_msg in msg:
            print("Startup message detected, ignoring...")
            start_time = time.ticks_ms()
            byte_sequence = b''

            while True:
                if self._uart.any():
                    byte_sequence += self._uart.read()  # 디코드 제거
                    print(f"Processing: {byte_sequence}")
                    if byte_sequence[-len(end_msg):] == end_msg:
                        print("Detected special ending sequence. Stopping the loop.")
                        break

                elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
                if elapsed_time > timeout_duration:
                    print("Timeout reached. Ending the loop without detecting end_msg.")
                    break
            return True
        return False
    
    def command_check_hex_data (self, command_id):

        start_time = time.ticks_ms()
        timeout_duration= 2000
        command_hex = b''

        while True:
            if self._uart.any():
                command_hex= self._uart.read()
                print(f"Hex data: {command_hex}")
                if int(command_hex[0:]) == command_id:
                    break
                else:
                    print(f"not matched hex data ({command_hex}:{commnad_id})")
                    
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            if elapsed_time > timeout_duration:
                print("Timeout reached. Ending the loop without detecting end_msg.")
                break
        return

    def command_parsing(self, message):
        if message.strip() == b'.' or self.command_check_device_start(message):
            self.set_xmos_status_active()            
            return None        
        try:
            parts = message.decode().strip('\\r\\n').split(',')
            if len(parts) < 5:
                raise ValueError("failed to parsing command")

            command = parts[0]
            id = int(parts[1].split('=')[1])
            score = int(parts[2].split('=')[1])
            sg_diff = int(parts[3].split('=')[1])
            energy = int(parts[4].split('=')[1])

            #print(f"Command: {command}, ID: {id}, Score: {score}, SG_Diff: {sg_diff}, Energy: {energy}")
            #self.command_check_hex_data(id)
            self.set_xmos_status_active()

        except Exception as e:
            print(f"Error parsing message: {e}")
            return None

        data = {
            "command": command,
            "id": id,
            "xmos_status": self.xmos_active
        }
        
        return json.dumps(data)


    def command_uart_from_xmos_bypass(self):
        if not self._uart.any():
            return None

        while self._uart.any():
            send_msg += self._uart.read()
        
        return send_msg

    def command_uart_from_xmos_parsing(self):
        status_data= self.check_xmos_status_timeout()
        if status_data:
            return status_data

        if not self._uart.any():
            return None

        message = self._uart.read()
        send_msg = self.command_parsing(message)

        return send_msg