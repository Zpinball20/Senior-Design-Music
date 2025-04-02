import serial
import time
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QTimer

arduino = serial.Serial(port='COM5',   baudrate=115200, timeout=.1) #port name is subject to change

class py_to_arduino(QObject):
    raw_arduino_data = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()

    @Slot(bool)
    def record_audio(self, input: bool):
        arduino.write(bytes(str(input), 'utf-8'))

        if(input == True):
            self.timer.start(500)
            print("Now recording")
            dataArd = arduino.readline().decode('utf-8').strip()
            print(dataArd)

        if(input == False):
            self.timer.start(500)
            dataArd = arduino.readline().decode('utf-8').strip()
            print(dataArd)
            data = [
                {"pitch": "C", "accidental": "", "octave": 4, "duration": 1},
                {"pitch": "D", "accidental": "", "octave": 4, "duration": 2},
                {"pitch": "E", "accidental": "", "octave": 4, "duration": 0.5},
                {"pitch": "F", "accidental": "", "octave": 4, "duration": 0.5}
            ]

            #self.raw_arduino_data.emit(data)
            print("End Recording")