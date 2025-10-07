import serial
import time
from threading import Timer

class ShutterController:
    def __init__(self, port: str, baud_rate: int):
        self.timer = None
        self.port = port
        self.baud_rate = baud_rate
        self.ser = self.connect()

    def connect(self):
        serial_connection = serial.Serial(self.port, self.baud_rate)
        time.sleep(2)
        return serial_connection

    def close(self):
        self.ser.flush()
        self.ser.close()

    def open_shutter(self):
        self.ser.write(b'1')
        print(self.ser.readline().decode())

    def close_shutter(self):
        self.ser.write(b'0')
        print(self.ser.readline().decode())

    def get_status(self):
        self.ser.write(b'?')
        status = int(self.ser.readline().decode())
        print(status)
        return status

    def timed_exposure(self, exposure_time: float, time_unit = "s"):
        if time_unit == "ms":
            exposure_time = exposure_time / 1000.0
        elif time_unit == "s":
            pass
        elif time_unit == "min":
            exposure_time = exposure_time * 60.0
        elif time_unit == "h":
            exposure_time = exposure_time * 3600.0
        else:
            raise NotImplementedError

        self.timer = Timer(exposure_time, self.close_shutter)

        self.open_shutter()
        self.timer.start()

    def abort_timed_exposure(self):
        print("Aborting exposure")
        if self.timer is not None:
            self.timer.cancel()
            self.close_shutter()
