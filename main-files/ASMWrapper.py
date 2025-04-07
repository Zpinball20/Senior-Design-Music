from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication
from convertArduinoData import convertArudinoData
from ASMController import ASMController
from appView import MainApplication
from pythonToArduino import py_to_arduino
from MusicXMLToMIDI import toMIDI
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(), 'main-files'))

def main():
    app = QApplication(sys.argv)

    arduinoConverter = convertArudinoData()
    view = MainApplication()
    arduinoComm = py_to_arduino()
    midiConverter = toMIDI()
    controller = ASMController(arduinoConverter, view, arduinoComm, midiConverter)

    view.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()