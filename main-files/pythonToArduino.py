import serial
import time
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot, QTimer

arduino = serial.Serial(port='COM5',   baudrate=115200, timeout=.1) #port name is subject to change

class py_to_arduino(QObject):
    raw_arduino_data = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.pitch = ""
        self.accidental = ""
        self.octave = ""
        self.beatLengthRounded = 0.0

    @Slot(bool)
    def record_audio(self, input: bool):
        arduino.write(bytes(str(input), 'utf-8'))

        if(input == True):
            self.timer.start(500)
            print("Now recording")

        if(input == False):
            self.timer.start(500)
            data = self.parseData()
            #print(dataArd)
            #data = [
            #    {"pitch": "C", "accidental": "", "octave": 4, "duration": 1},
            #    {"pitch": "", "accidental": "", "octave": 4, "duration": 2},
            #    {"pitch": "E", "accidental": "", "octave": 4, "duration": 0.5},
            #    {"pitch": "F", "accidental": "", "octave": 4, "duration": 0.5}
            #]

            self.raw_arduino_data.emit(data)
            print("End Recording")

    def parseData(self):
        data = []  # Initialize an empty list to store the parsed data

        while True:
            note = arduino.readline().decode('utf-8').strip()  # Read note
            duration = arduino.readline().decode('utf-8').strip()  # Read duration

            print(note)
            print(duration)

            if not note or not duration:  # Break out of loop if no data
                break

            parsed_note = {}

            if note == "rest" or note == "Rest":
                parsed_note["pitch"] = ""
                parsed_note["accidental"] = ""
                parsed_note["octave"] = ""
            else:
                parsed_note["pitch"] = note[0]
                parsed_note["accidental"] = note[1] if len(note) > 1 else ""
                parsed_note["octave"] = int(note[2]) if len(note) > 2 else 4  # Default octave to 4 if not provided

            beatLength = float(duration) * 2
            parsed_note["duration"] = round(beatLength) / 2  # Round to nearest 0.5 interval

            # Append the parsed note to the list
            data.append(parsed_note)

        return data  # Return the accumulated list of notes
