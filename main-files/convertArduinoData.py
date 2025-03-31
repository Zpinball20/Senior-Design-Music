from music21 import stream, note, meter, key, tempo
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
import subprocess

class convertArudinoData(QObject):

    def __init__(self):
        super().__init__()
        self.xmlFileName = None
        self.outputFilePath = None

    @Slot(str)
    def set_musicxml_file_name(self, name: str):
        self.xmlFileName = name + ".musicxml"
        #print(self.xmlFileName)

    @Slot(str)
    def set_output_file_path(self, path: str):
        self.outputFilePath = path
        #print(self.outputFilePath)

    @Slot(list)
    def process_external_data(self, data: list):
        print("This function has been called")
        score = stream.Score()
        part = stream.Part()

        ## TO BE REMOVED LATER (TEST DATA) ##

        #fp='testMusic.musicxml'

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

            # Start new measure if current one more than 4 beats (this will be dynamic later)
            if current_duration >= 4:
                part.append(measure)
                measure = stream.Measure()
                current_duration = 0

        # Add the last measure if not empty
        if len(measure.notes) > 0:
            part.append(measure)

        score.append(part)
        score.write('musicxml', self.xmlFileName)

        self.convert_to_pdf(self.outputFilePath)



### Terminal call to MuseScore4.exe
    def convert_to_pdf(self):

        #MuseScore exe
        mscore_path = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"
        
        command = [mscore_path, self.xmlFileName, "-o", self.outputFilePath]
        
        try:
            subprocess.run(command, check=True)
            print(f"Conversion successful! PDF saved at {self.outputFilePath}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")


    #Plans for future
    #Determine key signature if not defined by user
    #take input for bpm