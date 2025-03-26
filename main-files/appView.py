from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QButtonGroup,
                             QLineEdit, QGroupBox, QFormLayout, QGridLayout, QComboBox, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QRadioButton, QHBoxLayout, QApplication, QStackedWidget)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
import sys

class MainApplication(QWidget):
    convertAudioIntoSheetMusic = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 400, 300)

        self.stack = QStackedWidget(self)

        self.main_menu = QWidget()
        self.audioMenu = audioMenu(self)
        self.midiMenu = midiMenu(self)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.audioMenu)
        self.stack.addWidget(self.midiMenu)

        main_layout = QVBoxLayout()

        button1 = QPushButton("Convert Live Audio to Sheet Music")
        button1.clicked.connect(lambda: self.stack.setCurrentWidget(self.audioMenu))

        button2 = QPushButton("Convert Sheet Music to MIDI")
        button2.clicked.connect(lambda: self.stack.setCurrentWidget(self.midiMenu))

        main_layout.addWidget(button1)
        main_layout.addWidget(button2)

        self.main_menu.setLayout(main_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        self.stack.setCurrentWidget(self.main_menu)

        self.send_go_signal = self.audioMenu.record_signal

class audioMenu(QWidget):
    record_signal = Signal(bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.recording = False

        back_button = QPushButton("← Back")
        back_button.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_menu))

        label = QLabel("Convert Audio to Sheet Music")

        toggle_recording_button = QPushButton("Start Recording")
        toggle_recording_button.clicked.connect(self.toggle_recording)

        layout.addWidget(back_button)
        layout.addWidget(label)
        layout.addWidget(toggle_recording_button)
        self.setLayout(layout)

    def toggle_recording(self):
        self.recording = not self.recording
        self.record_signal.emit(self.recording)

class midiMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        back_button = QPushButton("← Back")
        back_button.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_menu))

        label = QLabel("This is Menu 2")

        layout.addWidget(back_button)
        layout.addWidget(label)
        self.setLayout(layout)
