from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, reader, api, viewer, arduinoComm, midiConverter):
        super().__init__()
        self.convertArudinoData = reader
        self.toAPI = api
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
        self.view.input_pdf_file.connect(self.midiConverter.set_input_filepath)
        self.view.output_midi_file.connect(self.midiConverter.set_output_filepath)
        self.view.wrkingDir.connect(self.midiConverter.set_directory)