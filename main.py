import os
import sys

import requests
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QButtonGroup, QRadioButton
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PIL import Image
import math

SCREEN_SIZE = [800, 600]


# maptype = 'map'


class Example(QMainWindow):
    def __init__(self):
        self.a = 'map'

        super().__init__()
        uic.loadUi('wind.ui', self)
        self.getimage()
        self.initUI()
        self.pushButton.clicked.connect(self.getimage)
        self.SCHEMA.clicked.connect(self.SHM)
        self.HYBRIT.clicked.connect(self.HYB)
        self.SPYTNIK.clicked.connect(self.SPY)

        self.types_maps = {
            'SCHEMA': 'map',
            'HYBRIT': 'sat',
            'SPYTNIK': 'skl'
        }

    def SHM(self):
        self.a = self.types_maps['SCHEMA']
        print(self.a)

    def HYB(self):
        self.a = self.types_maps['HYBRIT']
        print(self.a)

    def SPY(self):
        self.a = self.types_maps['SPYTNIK']
        print(self.a)

    def getimage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response_params = {
            'll': f'{float(self.Xedit.toPlainText())},{float(self.Yedit.toPlainText())}',
            'spn': f'{float(self.sizeEdit.toPlainText())},{float(self.sizeEdit.toPlainText())}',
            'l': self.a
        }
        response = requests.get(map_request, params=response_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        myimg = Image.open('map.png')
        myimg.save('map.png', 'png')
        self.showImage()

    def initUI(self):
        self.setGeometry(150, 150, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap("map.png")
        self.map.move(0, 0)
        self.map.resize(500, 400)
        self.map.setPixmap(self.pixmap)

    def showImage(self):
        self.map_file = 'map.png'
        self.pixmap = QPixmap('map.png')
        self.map.move(0, 0)
        self.map.resize(500, 400)
        self.map.setPixmap(self.pixmap)

    def keyPressEvent(self, event: QKeyEvent):

        match event.key():
            case Qt.Key.Key_L:
                self.scaleUp()
            case Qt.Key.Key_O:
                self.scaleDown()
            case Qt.Key.Key_PageUp:
                self.scaleUp()
            case Qt.Key.Key_PageDown:
                self.scaleDown()
            case Qt.Key.Key_U:
                self.movebydir(0, 1)
            case Qt.Key.Key_H:
                self.movebydir(1, 0)
            case Qt.Key.Key_J:
                self.movebydir(0, -1)
            case Qt.Key.Key_K:
                self.movebydir(-1, 0)

    def movebydir(self, x, y):
        a = float(self.xEdit.toPlainText())
        b = float(self.yEdit.toPlainText())
        a += x
        b += y
        if 0 < a < 200:
            self.sizeEdit.setText(1)
            self.getimage()
        if 0 < b < 200:
            self.sizeEdit.setText(1)
            self.getimage()

    def scaleUp(self):
        a = float(self.sizeEdit.toPlainText())
        a += 3
        if a < 60:
            self.sizeEdit.setText(str(a))
            self.getimage()

    def scaleDown(self):
        a = float(self.sizeEdit.toPlainText())
        if a > 4:
            a -= 3
            self.sizeEdit.setText(str(a))
            self.getimage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        # os.remove(self.map_file)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.excepthook = sys.excepthook
    ex.show()
    sys.exit(app.exec())
