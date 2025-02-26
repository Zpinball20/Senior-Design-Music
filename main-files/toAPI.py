import requests
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

class toAPI():

    @Slot(str)
    def upload_musicxml_to_api(file_path):
        print("upload function successfully called")