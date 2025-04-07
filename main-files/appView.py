from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QButtonGroup,
                             QLineEdit, QGroupBox, QFormLayout, QGridLayout, QComboBox, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QRadioButton, QHBoxLayout, QApplication, QStackedWidget, QFileDialog)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
import os

class MainApplication(QWidget):

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

        # Audio --> Sheet Music Signals
        self.send_go_signal = self.audioMenu.record_signal
        self.sheetMusicSavePath = self.audioMenu.sheet_music_save_path
        self.fileName = self.audioMenu.name_of_file
        self.scoreNameSignal = self.audioMenu.score_name_signal
        self.composerNameSignal = self.audioMenu.composer_name_signal

        # Sheet Music --> MIDI Signals
        self.inputFileLocation = self.midiMenu.inputPdfFile
        self.output_midi_file = self.midiMenu.outputFileLocation
        self.wrkingDir = self.midiMenu.working_directory
        self.runConv = self.midiMenu.run_conversion

class audioMenu(QWidget):
    record_signal = Signal(bool)
    sheet_music_save_path = Signal(str) # Signal for save location of pdf (audio into sheet music)
    name_of_file = Signal(str) # signal for base name of file
    score_name_signal = Signal(str)
    composer_name_signal = Signal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.recording = False
        self.save_path = None # Save path of the pdf
        self.sheet_music_file_name = None # base name of file
        self.score_name = ""
        self.composer_name = ""

        layout = QVBoxLayout()

        back_button = QPushButton("← RETURN TO MAIN MENU")
        back_button.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_menu))

        label = QLabel("Convert Audio to Sheet Music")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter the title of your score")

        save_title_button = QPushButton("Save Title Name")
        save_title_button.clicked.connect(self.setScoreName)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name (composer)")

        save_name_button = QPushButton("Save Composer Name")
        save_name_button.clicked.connect(self.setComposerName)

        save_as_button = QPushButton("Save As...")
        save_as_button.clicked.connect(self.choose_save_location)

        self.save_location_label = QLabel("No file selected")  # Label to display the chosen file path

        self.toggle_recording_button = QPushButton("Start Recording")
        self.toggle_recording_button.clicked.connect(self.toggle_recording)

        layout.addWidget(back_button)
        layout.addWidget(label)
        layout.addWidget(self.title_input)
        layout.addWidget(save_title_button)
        layout.addWidget(self.name_input)
        layout.addWidget(save_name_button)
        layout.addWidget(save_as_button)
        layout.addWidget(self.save_location_label)
        layout.addWidget(self.toggle_recording_button)
        self.setLayout(layout)

    def toggle_recording(self):
        self.recording = not self.recording
        self.record_signal.emit(self.recording)

        if self.recording:
            self.toggle_recording_button.setText("Stop Recording")
        else:
            self.toggle_recording_button.setText("Start Recording")

    def choose_save_location(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save As", 
            "", 
            "PDF (*.pdf);;All Files (*.*)"
        )
        if file_path:
            self.save_path = file_path
            self.file_name = os.path.splitext(os.path.basename(file_path))[0]
            self.save_location_label.setText(f"Saving to: {self.save_path}")

            #Emit signals to be used in saving the pdf
            self.sheet_music_save_path.emit(self.save_path)
            self.name_of_file.emit(self.file_name)

    def setScoreName(self):
        self.score_name = self.title_input.text()
        self.score_name_signal.emit(self.score_name)
    
    def setComposerName(self):
        self.composer_name = self.name_input.text()
        self.composer_name_signal.emit(self.composer_name)

class midiMenu(QWidget):

    inputPdfFile = Signal(str)
    outputFileLocation = Signal(str)
    working_directory = Signal(str)
    run_conversion = Signal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.input_file = None
        self.output_file = None

        layout = QVBoxLayout()

        back_button = QPushButton("← RETURN TO MAIN MENU")
        back_button.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_menu))

        label = QLabel("Convert Sheet Music to MIDI")

        # Input file selection (PDF only)
        input_button = QPushButton("Select PDF File")
        input_button.clicked.connect(self.select_input_file)
        self.input_label = QLabel("No input file selected")

        # Output file selection
        output_button = QPushButton("Select Output Destination")
        output_button.clicked.connect(self.select_output_file)
        self.output_label = QLabel("No output file selected")

        # Run Conversion button
        to_midi_button = QPushButton("Convert to MIDI")
        output_button.clicked.connect(self.send_conversion_signal)

        layout.addWidget(back_button)
        layout.addWidget(label)
        layout.addWidget(input_button)
        layout.addWidget(self.input_label)
        layout.addWidget(output_button)
        layout.addWidget(self.output_label)
        layout.addWidget(to_midi_button)
        self.setLayout(layout)

    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.input_file = file_path
            self.input_label.setText(f"Input: {os.path.basename(file_path)}")
            self.inputPdfFile.emit(self.input_file)


    def select_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output Destination", "", 
            "MIDI Files (*.mid);;All Files (*.*)"
        )
        if file_path:
            self.output_file = file_path
            self.output_label.setText(f"Output: {os.path.basename(file_path)}")
            self.outputFileLocation.emit(self.output_file)
            self.working_directory.emit(os.path.dirname(self.output_file))

    def send_conversion_signal(self):
        if(self.input_file != None and self.output_file != None):
            self.run_conversion.emit()