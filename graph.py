import math
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MplWidget(QWidget):  # Класс виджета для графика
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


class GraphMain(QWidget):
    def __init__(self, win_title: str, win_icon: str, ui_file: str, data: tuple, screen_geometry: tuple, parent=None):
        QWidget.__init__(self, parent)
        designer_file = QFile(ui_file)
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget)
        self.ui = loader.load(designer_file, self)
        designer_file.close()
        self.setWindowTitle(win_title)
        self.setWindowIcon(QIcon(win_icon))
        self.setMinimumSize(screen_geometry[0] // 2, screen_geometry[1] // 2)
        self.setMaximumSize(screen_geometry[0] // 2, screen_geometry[1] // 2)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

        self.data = data
        self.screen_geometry = screen_geometry

    def get_data(self, index_data: int):
        x = []
        y = []
        for i in range(1, 29999):
            x.append(abs(float(self.data[i][index_data])))
            y.append(int(self.data[i][0]))

        return x, y


class HistWin(GraphMain):
    def __init__(self, win_title: str, win_icon: str, index_data: int, ui_file: str, data: tuple, screen_geometry: tuple, parent=None):
        GraphMain.__init__(self, win_title, win_icon, ui_file, data, screen_geometry, parent)

        self.create_hist(win_title, index_data)
        self.ui.lineEdit.setText(str(self.quadratic_mean(index_data)))

    def separate_x_axe(self, index_data):
        data = self.get_data(index_data)
        y = []
        idx = 0

        max_x = max(data[0])
        max_del = max_x / 53
        x = [0 for _ in range(53)]
        for elem in data[0]:
            for i in range(53):
                if (max_del * i) <= elem <= (max_del * (i + 1)):
                    x[i] += 1

        for i in range(len(x)):
            if x[i] != 0:
                idx = i
                break

        for i in range(idx, len(x)):
            y.append(i * max_del)

        return x[idx:], y, idx

    def create_hist(self, win_title: str, index_data: int):
        x, y, idx = self.separate_x_axe(index_data)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.stairs(x[:(52 - idx)], y, label=f'graph {win_title} modulo')
        self.ui.asss.canvas.axes.legend()
        self.ui.asss.canvas.axes.set_title(win_title)
        self.ui.asss.canvas.draw()

    def quadratic_mean(self, index_data: int):
        data = self.get_data(index_data)
        n = data[1][-1]

        summ = sum(data[0])
        arithmetic_mean = summ / (n + 1)

        cf = 0
        for num in data[0]:
            cf += math.pow((num - arithmetic_mean), 2)

        s = math.sqrt(cf / n)
        return s


class PhDifWin(GraphMain):
    def __init__(self, win_title: str, win_icon: str, index_data: int, ui_file: str, data: tuple, screen_geometry: tuple, parent=None):
        GraphMain.__init__(self, win_title, win_icon, ui_file, data, screen_geometry, parent)

        self.create_graph(win_title, index_data)

    def create_graph(self, win_title: str, index_data: int):
        y, x = self.get_data(index_data)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.plot(x, y)
        self.ui.asss.canvas.axes.set_title(win_title)
        self.ui.asss.canvas.draw()


class CorrelationWin(GraphMain):
    def __init__(self, win_title: str, win_icon: str, ui_file: str, data: tuple, screen_geometry: tuple, parent=None):
        GraphMain.__init__(self, win_title, win_icon, ui_file, data, screen_geometry, parent)

        self.data1 = self.get_data(data[0])
        self.data2 = self.get_data(data[1])
        self.create_graph(win_title)

    def get_data(self, data: tuple):
        x = []
        y = []
        key = data[1]

        if key == 1:
            for i in range(0, 20):
                x.append(int(data[0][i][1]))
                y.append(float(data[0][i][0]))

        else:
            for i in range(0, 20):
                x.append(int(data[1][i]))
                y.append(float(data[0][i]))

        return y, x

    def create_graph(self, win_title: str):
        y1, x1 = self.data1
        y2, x2 = self.data2

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.plot(x1, y1, label='Chanel 1')
        self.ui.asss.canvas.axes.plot(x2, y2, label='Chanel 2')
        self.ui.asss.canvas.axes.legend()
        self.ui.asss.canvas.axes.set_title(win_title)
        self.ui.asss.canvas.draw()
