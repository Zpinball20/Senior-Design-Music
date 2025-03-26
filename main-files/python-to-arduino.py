import serial
import time
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QTimer

arduino = serial.Serial(port='COM4',   baudrate=115200, timeout=.1) #port name is subject to change

class py_to_arduino(QObject):
    def __init__(self):
        super().__init__()

    raw_arduino_data = Signal(str)

    @Slot(bool)
    def record_signal(self, input: bool):
        arduino.write(bytes(str(input), 'utf-8'))

        if(input == True):
            self.timer.start(500)

        if(input == False):
            self.timer.start(500)
            data = arduino.readline().decode('utf-8').strip()
            self.raw_arduino_data.emit(data)
