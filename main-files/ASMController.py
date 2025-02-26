from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, reader, api, viewer):
        super().__init__()
        self.readArudinoData = reader
        self.toAPI = api
        self.view = viewer

        # Call function to convert data into MusicXML
        self.view.convertAudioIntoSheetMusic.connect(self.readArudinoData.process_external_data)

        # Send file path to API
        self.readArudinoData.xml_file_path.connect(self.toAPI.upload_musicxml_to_api)