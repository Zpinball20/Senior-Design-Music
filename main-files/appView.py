from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QButtonGroup,
                             QLineEdit, QGroupBox, QFormLayout, QGridLayout, QComboBox, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QRadioButton, QHBoxLayout, QApplication)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
import sys

class MainApplication(QWidget):
    convertAudioIntoSheetMusic = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Button App")

        layout = QVBoxLayout()
        self.button = QPushButton("Button")
        self.button.clicked.connect(self.convertAudioData)

        layout.addWidget(self.button)

        self.setLayout(layout)

    @Slot()
    def convertAudioData(self):
        self.convertAudioIntoSheetMusic.emit()
        print("button pressed")

app = QApplication(sys.argv)
window = MainApplication()
window.show()
sys.exit(app.exec())
