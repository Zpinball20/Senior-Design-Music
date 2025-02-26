from music21 import stream, note, meter, key, tempo
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

external_data = [
        {"pitch": "C", "accidental": "#", "octave": 4, "duration": 1},
        {"pitch": "F", "accidental": "", "octave": 4, "duration": 2},
        {"pitch": "B", "accidental": "-", "octave": 3, "duration": 0.5},
        {"pitch": "A", "accidental": "", "octave": 5, "duration": 4}
    ]

class readArudinoData(QObject):

    xml_file_path = Signal(str)

    def __init__(self):
        super().__init__()

    @Slot()
    def process_external_data(self):
        print("This function has been called")
        score = stream.Score()
        part = stream.Part()

        ## TO BE REMOVED LATER (TEST DATA) ##
        data = [
            {"pitch": "C", "accidental": "#", "octave": 4, "duration": 1},
            {"pitch": "F", "accidental": "", "octave": 4, "duration": 2},
            {"pitch": "B", "accidental": "-", "octave": 3, "duration": 0.5},
            {"pitch": "A", "accidental": "", "octave": 5, "duration": 4}
        ]

        fp='testMusic.musicxml'

        bpm = 90

        ######################################

        # time sig and key sig
        part.append(meter.TimeSignature('4/4'))
        part.append(key.KeySignature(0))  # C maj

        measure = stream.Measure()
        current_duration = 0 

        for item in data:
            pitch = item['pitch']
            accidental = item['accidental']
            octave = item['octave']
            duration = item['duration']

            full_pitch = f"{pitch}{accidental}{octave}"
            n = note.Note(full_pitch)
            n.quarterLength = duration

            metronome = tempo.MetronomeMark(number=bpm)  # set BPM
            part.append(metronome)

            # Add note to measure
            measure.append(n)
            current_duration += duration

            # Start a new measure if current one exceeds 4 beats
            if current_duration >= 4:
                part.append(measure)
                measure = stream.Measure()
                current_duration = 0

        # Add the last measure if it's not empty
        if len(measure.notes) > 0:
            part.append(measure)

        score.append(part)
        score.write('musicxml', fp)

        self.xml_file_path.emit(fp)

    #Plans for future
    #Determine key signature if not defined by user
    #take input for bpm

#convertToXML().process_external_data(external_data, fp, bpm = 90)