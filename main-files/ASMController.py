from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, readArudinoData, toAPI, view):
        super().__init__()
        self.readArudinoData = readArudinoData
        self.toAPI = toAPI
        self.view = view

        # Call function to convert data into MusicXML
        self.view.convertAudioIntoSheetMusic.connect(self.readArudinoData.process_external_data)

        # Send file path to API
        self.readArudinoData.xml_file_path.connect(self.toAPI.upload_musicxml_to_api)