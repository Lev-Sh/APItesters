import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QTextEdit, QPushButton
from PyQt5 import uic
from PIL import Image

SCREEN_SIZE = [800, 600]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('wind.ui', self)
        self.getimage()
        self.initUI()
        self.pushButton.clicked.connect(self.getimage)

    def getimage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response_params = {
            'll': f'{float(self.Xedit.toPlainText())},{float(self.Yedit.toPlainText())}',
            'spn': f'{float(self.sizeEdit.toPlainText())},{float(self.sizeEdit.toPlainText())}',
            'l': 'map'
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

