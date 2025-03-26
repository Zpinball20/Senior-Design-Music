from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, reader, api, viewer, arduinoComm):
        super().__init__()
        self.convertArudinoData = reader
        self.toAPI = api
        self.view = viewer
        self.serialReader = arduinoComm

        # Call function to begin or end recording live audio
        self.view.send_go_signal.connect(self.serialReader.record_audio)

        # Send data from ardunio to converter
        self.serialReader.raw_arduino_data.connect(self.convertArudinoData.process_external_data)

        # Send file path to API
        self.convertArudinoData.xml_file_path.connect(self.toAPI.upload_musicxml_to_api)