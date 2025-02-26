from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication
from readArduinoData import readArudinoData
from toAPI import toAPI
from ASMController import ASMController
from appView import MainApplication
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(), 'main-files'))


def main():
    app = QApplication(sys.argv)

    reader = readArudinoData()
    api = toAPI()
    view = MainApplication()
    controller = ASMController(reader, api, view)

    view.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()