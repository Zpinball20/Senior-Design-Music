from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, reader, viewer, arduinoComm, midiConverter):
        super().__init__()
        self.convertArudinoData = reader
        self.view = viewer
        self.serialReader = arduinoComm
        self.midiConverter = midiConverter

        # Call function to begin or end recording live audio
        self.view.send_go_signal.connect(self.serialReader.record_audio)

        # Send data from ardunio to converter
        self.serialReader.raw_arduino_data.connect(self.convertArudinoData.process_external_data)

        #Send user information for file saving the Audio --> Sheet Music
        self.view.sheetMusicSavePath.connect(self.convertArudinoData.set_output_file_path)
        self.view.fileName.connect(self.convertArudinoData.set_musicxml_file_name)

        #Send user information for file saving the Sheet Music --> MIDI
        self.view.inputFileLocation.connect(self.midiConverter.setInputFilePath)
        self.view.output_midi_file.connect(self.midiConverter.setOutputFilePath)
        self.view.wrkingDir.connect(self.midiConverter.setDirectory)
        self.view.runConv.connect(self.midiConverter.convert_toMIDI)