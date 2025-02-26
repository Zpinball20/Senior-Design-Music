from PyQt6.QtCore import QObject

class ASMController(QObject):
    def __init__(self, readArudinoData, toAPI, view):
        super().__init__()
        self.readArudinoData = readArudinoData
        self.toAPI = toAPI
        self.view = view

        # Send file path to API
        self.readArudinoData.xml_file_path.connect(self.toAPI.upload_musicxml_to_api)