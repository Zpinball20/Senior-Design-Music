import requests
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

class toAPI(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str)
    def upload_musicxml_to_api(self, file_path: str):
        print("upload function successfully called")