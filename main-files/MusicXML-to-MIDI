from music21 import converter
from PyQt6.QtCore import QObject

class toMIDI(QObject):
    def __init__(self):
        super().__init__

    def convert_toMIDI(self, xml_file: str, midi_file: str):
        try:

            xml_file = converter.parse(xml_file)
            
            xml_file.write('midi', midi_file)
            
            print(f"Successfully converted {xml_file} to {midi_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")

# function call
toMIDI().convert_toMIDI("testMusic.musicxml", "output.mid")
