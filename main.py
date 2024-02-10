from PySide2.QtWidgets import *
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from graph import HistWin, PhDifWin, CorrelationWin
from ohata import OhataWin
import sys
import time
import os
from excel_opener import open_txt, open_correlation_txt, create_correlation_txt
import tkinter as tk
from tkinter.filedialog import askopenfilename


class MainWin(QWidget):
    def __init__(self, width: int, height: int, parent=None):
        QWidget.__init__(self, parent)
        designer_file = QFile("main.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(designer_file, self)
        designer_file.close()
        self.error = QErrorMessage(self)
        self.msg_info = QMessageBox(self)
        self.setWindowTitle("Excel Jxxx File Opener")
        self.screen_geometry = (width, height)
        self.setMinimumSize(width//4, height//7)
        self.setMaximumSize(width//4, height//7)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

        self.file_name = ''
        self.data = tuple()

        self.ui.label_file.setText("Выберите файл для работы")

        self.ui.button_ohata.clicked.connect(self.open_ohata)
        self.ui.button_graph.clicked.connect(self.open_graph)
        self.ui.button_file.clicked.connect(self.open_file_jxxx)

    def open_ohata(self):
        self.win = OhataWin(self.screen_geometry)
        self.win.show()

    def show_msg_info(self, msg: str, title: str):
        self.msg_info.setWindowTitle(title)
        self.msg_info.setText(msg)
        self.msg_info.setIcon(QMessageBox.Information)
        self.msg_info.show()

    def ms_error(self, title: str, message: str, type_error: str):  # Создание окна ошибки
        self.error.setWindowTitle(title)
        self.error.showMessage(message, type_error)

    def open_file_jxxx(self):
        root = tk.Tk()
        root.withdraw()

        filetypes = (("Excel файл", "*.xlsx"),)
        file_path = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        idx = file_path.rfind('/')
        file_name = file_path[idx+1:]

        if file_name:
            self.ui.label_file.setText(f"Работа с файлом '{file_name}'")
            self.file_name = file_name
            self.data = open_txt(self.file_name, file_name)

            idx = file_name.rfind('.')
            self.show_msg_info(f"Файл '{file_path}' был открыт. Данные записаны в "
                               f"'{file_name[:idx]}/data_{file_name}.txt'", 'Открытие файла')

    def open_graph(self):
        data = tuple()
        try:
            data = self.create_correlation_data()
        except IndexError:
            self.ms_error('Ошибка открытия файла', 'Не был выбран файл!', 'IndexError')

        if data:
            self.hist_ch1 = HistWin('Chanel 1', 1, 'hist2.ui', self.data, self.screen_geometry)
            self.hist_ch2 = HistWin('Chanel 2', 2, 'hist2.ui', self.data, self.screen_geometry)
            self.ph_dif = PhDifWin('Phase difference', 3, 'hist.ui', self.data, self.screen_geometry)
            self.correlation = CorrelationWin('Correlation', 'hist.ui', data, self.screen_geometry)

            self.hist_ch1.show()
            self.hist_ch2.show()
            self.ph_dif.show()
            self.correlation.show()

            self.hist_ch1.move(0, 0)
            self.hist_ch2.move(self.screen_geometry[0]//2, 0)
            self.ph_dif.move(0, self.screen_geometry[1]//2)
            self.correlation.move(self.screen_geometry[0]//2, self.screen_geometry[1]//2)

    def get_data(self, index_data: int):
        x = []
        y = []
        for i in range(1, 29999):
            x.append(abs(float(self.data[i][index_data])))
            y.append(int(self.data[i][0]))

        return x, y

    def create_correlation(self, index_data: int):
        data = self.get_data(index_data)

        lags = range(20)
        correlation = len(lags) * [0]
        mean = sum(data[0]) / len(data[0])
        var = sum([(x - mean) ** 2 for x in data[0]]) / len(data[0])
        new_data = [x - mean for x in data[0]]

        for lag in lags:
            c = 1
            if lag > 0:
                tmp = [(new_data[lag:][i] * new_data[:-lag][i]) for i in range(len(data[0]) - lag)]
                c = sum(tmp) / len(data[0]) / var
                self.ui.progressBar.setValue((lag * 100) / len(lags))
            correlation[lag] = c

        x = [i for i in range(len(correlation))]

        time.sleep(1)
        create_correlation_txt((correlation, x), index_data, self.file_name)

        self.ui.progressBar.setValue(0)

        return correlation, x, 0

    def create_correlation_data(self):
        idx = self.file_name.rfind('.')

        if not os.path.exists(f'{self.file_name[:idx]}/correlation_txt1_{self.file_name}.txt'):
            data1 = self.create_correlation(1)
        else:
            data1 = open_correlation_txt(1, self.file_name)

        if not os.path.exists(f'{self.file_name[:idx]}/correlation_txt2_{self.file_name}.txt'):
            data2 = self.create_correlation(2)
        else:
            data2 = open_correlation_txt(2, self.file_name)

        return data1, data2

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Выход из программы",
            "Вы хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            os.system("taskkill /f /im Excel_Jxxx_File_Opener.exe")
        else:
            event.ignore()


def start_program():
    app = QApplication(sys.argv)
    screen_rect = app.primaryScreen().availableGeometry()
    window = MainWin(screen_rect.width(), screen_rect.height())
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_program()
