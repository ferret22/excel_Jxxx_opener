from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
from math import *


class OhataWin(QWidget):
    def __init__(self, screen_geometry: tuple, win_icon: str, parent=None):
        QWidget.__init__(self, parent)
        designer_file = QFile("UI/ohata.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(designer_file, self)
        designer_file.close()
        self.setWindowTitle("Модель Окамура-Хата")
        self.setWindowIcon(QIcon(win_icon))
        self.setMaximumSize(screen_geometry[0]//2, screen_geometry[1]//2.3)
        self.setMinimumSize(screen_geometry[0]//2, screen_geometry[1]//2.3)
        self.error = QErrorMessage(self)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)
        self.set_dialLine_text()
        self.ui.dial_f.valueChanged.connect(self.set_dialLine_text)
        self.ui.dial_ht.valueChanged.connect(self.set_dialLine_text)
        self.ui.dial_hr.valueChanged.connect(self.set_dialLine_text)
        self.ui.dial_r.valueChanged.connect(self.set_dialLine_text)

    def ms_error(self, title: str, message: str, type_error: str):  # Создание окна ошибкиf
        self.error.setWindowTitle(title)
        self.error.showMessage(message, type_error)

    def set_dialLine_text(self):
        self.ui.line_f.setText(str(self.ui.dial_f.value()))
        self.ui.line_ht.setText(str(self.ui.dial_ht.value()))
        self.ui.line_hr.setText(str(self.ui.dial_hr.value()))
        self.ui.line_r.setText(str(self.ui.dial_r.value()))
        self.calculate(self.get_data())

    def get_data(self):
        data = (int(self.ui.line_f.text()), int(self.ui.line_ht.text()), int(self.ui.line_hr.text()),
                int(self.ui.line_r.text()))
        return data

    def calculate(self, data):
        pt = 47
        log_f = log10(data[0])
        log_ht = log10(data[1])
        log_r = log10(data[3])

        alpha = (1.1 * log_f - 0.7) * data[2] - (1.56 * log_f - 0.8)
        kf = 4.78 * pow(log_f, 2) - 18.33 * log_f + 40.94

        answer = pt - 69.55 - 26.16 * log_f - (44.9 - 6.55 * log_ht) * log_r + 13.82 * log_ht + alpha + kf

        self.ui.line_answer.setText(str(answer))
