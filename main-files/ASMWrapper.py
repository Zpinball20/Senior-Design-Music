from PyQt6.QtCore import QObject
from readArduinoData import readArudinoData
from toAPI import toAPI
from ASMController import ASMController
from appView import MainApplication
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(), 'main-files'))

class ASMLogic:
    def __init__(self):
        super().__init__()

        self.readArudinoData = readArudinoData()
        self.toAPI = toAPI()
        self.view = MainApplication()
        self.ASMController = ASMController(self.readArudinoData, self.toAPI, self.view)