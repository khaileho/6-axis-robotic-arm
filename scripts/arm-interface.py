import serial
import json
import time

class MegaArmBridge:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2) # wait for mega to boot

    def send_targets(self, targets):
        """
        sends a list of 5 integers to the arduino mega
        example: [400, 0, 800, 0, 0]
        """
        packet = {"t": targets}
        json_packet = json.dumps(packet) # converts python dictionary into string of text
        self.ser.write(json_packet.encode('utf-8')) # converts the string to bytes
        print(f"sent: {json_packet}")

    def close(self):
        self.ser.close()

if __name__ == "__main__": # only run this code if main is ran
    # test execution
    arm = MegaArmBridge(port='COM3') # update to port
    arm.send_targets([1000, 0, 0, 0, 0])
    arm.close()