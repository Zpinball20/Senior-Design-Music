from music21 import converter
from PyQt6.QtCore import QObject, pyqtSlot as Slot
import subprocess
import os
import zipfile

class toMIDI(QObject):
    
    def __init__(self):
        super().__init__()
        self.inputFilePath = None #This is the file location of the PDF to be converted
        self.outputFilePath = None
        self.xmlFilePath = None
        self.currentDirectory = None

    @Slot(str)
    def setInputFilePath(self, path: str):
        self.inputFilePath = path
        print(self.inputFilePath)

    @Slot(str)
    def setOutputFilePath(self, path: str):
        self.outputFilePath = path
        print(self.outputFilePath)

    @Slot(str)
    def setDirectory(self, path: str):
        self.currentDirectory = path
        print(self.currentDirectory)

    @Slot()
    def convert_toMIDI(self):

        self.convert_pdf_to_musicxml()

        try:

            xml_file = converter.parse(self.xmlFilePath)
            
            xml_file.write('midi', self.outputFilePath)
            
            print(f"Successfully converted {xml_file} to {self.outputFilePath}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    #This ends up generating an xml file, which needs to be extracted
    def convert_pdf_to_musicxml(self):
        audiveris_path = r"C:\Program Files\Audiveris\bin\Audiveris.bat"  # Path to batch file
        command = [audiveris_path, "-batch", self.inputFilePath, "-export"]

        self.xmlFilePath = None  # Ensure it's always reset before conversion

        try:
            subprocess.run(command, check=True, shell=True)

            # Extract MusicXML files from any generated .mxl files
            for file in os.listdir(self.currentDirectory):
                if file.endswith(".mxl"):
                    mxl_file = os.path.join(self.currentDirectory, file)

                    with zipfile.ZipFile(mxl_file, 'r') as zip_ref:
                        zip_ref.extractall(self.currentDirectory)

            # Find .MusicXML file
            for extracted_file in os.listdir(self.currentDirectory):
                if extracted_file.endswith(".musicxml") or extracted_file.endswith(".xml"):
                    self.xmlFilePath = os.path.join(self.currentDirectory, extracted_file)
                    print(f"MusicXML file ready: {self.xmlFilePath}")
                    return  # Stop searching after first valid file

            print("No MusicXML file found.")

        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")