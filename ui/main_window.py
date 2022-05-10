from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QComboBox, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
from app_services.map_app_service import MapAppService
from services.ya_map_service import YaMapService
from domain.request import Request
import requests


class MainWindow(QWidget):
    def __init__(self, app_service: MapAppService, parent=None):
        super().__init__(parent)
        self.start = ['map', 37.530887, 55.703118, '37.530887,55.703118']
        self.app_service = app_service
        self.request = Request(self.start[0], self.start[1], self.start[2], self.start[3])
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 800)
        self.map_label = QLabel(self)
        self.map_box = QComboBox(self)
        self.label1 = QLabel(self)
        self.label1.setText('Вид карты:')
        self.label2 = QLabel(self)
        self.label2.setText('Место:')
        self.text = QLineEdit(self)
        self.adress = QLabel(self)
        self.post = QLabel(self)
        self.post_box = QCheckBox('Почтовый индекс', self)
        self.post_box.setChecked(False)
        self.map_box.addItems(['map'] + list(set(['sat', 'skl'])))
        self.pushbutton = QPushButton(self)
        self.pushbutton.setText('Искать')
        self.pushbutton.clicked.connect(self.click)
        self.pushButton = QPushButton(self)
        self.pushButton.setText('Сброс поискового результата')
        self.pushButton.clicked.connect(self.click1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.map_box)
        layout.addWidget(self.label2)
        layout.addWidget(self.text)
        layout.addWidget(self.post_box)
        layout.addWidget(self.adress)
        layout.addWidget(self.post)
        layout.addWidget(self.pushbutton)
        layout.addWidget(self.map_label)
        layout.addWidget(self.pushButton)

        self.setLayout(layout)
        self.show_map()

    def click(self):
        if self.text.text():
            response = requests.get(
                "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + self.text.text() + "&format=json")
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                if self.post_box.isChecked() is True:
                    post = toponym['metaDataProperty']['GeocoderMetaData']['Address']
                    if 'postal_code' in post:
                        self.post.setText('Почтовый индекс: ' + post['postal_code'])
                    else:
                        self.post.setText('Почтовый индекс не найден')
                else:
                    self.post.setText('')
                self.adress.setText('Адерс: ' + toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted'])
                toponym = toponym["Point"]["pos"]
                self.request = Request(self.map_box.currentText(), toponym.split()[0], toponym.split()[1],
                                       str(toponym.split()[0]) + ',' + str(toponym.split()[1]))
        else:
            self.request = Request(self.map_box.currentText(), self.request.get_longitude(),
                                   self.request.get_latitude(), self.request.get_sp_top())
        self.show_map()

    def click1(self):
        self.text.setText('')
        self.adress.setText('')
        self.post.setText('')
        self.post_box.setChecked(False)
        self.map_box.setCurrentText('map')
        self.request = Request(self.start[0], self.start[1], self.start[2], self.start[3])
        self.show_map()

    def show_map(self):
        map = self.app_service.execute(self.request)
        pixmap = QPixmap()
        if self.request.get_l() == 'map' or self.request.get_l() == 'skl':
            pixmap.loadFromData(map, 'PNG')
        elif self.request.get_l() == 'sat':
            pixmap.loadFromData(map, 'JPG')
        self.map_label.setPixmap(pixmap)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.request.up_zoom()
        elif key == Qt.Key.Key_PageDown:
            self.request.down_zoom()
        elif key == Qt.Key.Key_Left:
            self.request.left()
        elif key == Qt.Key.Key_Right:
            self.request.right()
        elif key == Qt.Key.Key_Up:
            self.request.up()
        elif key == Qt.Key.Key_Down:
            self.request.down()

        self.show_map()


if __name__ == '__main__':
    app = QApplication([])

    map_service = YaMapService()
    app_map_service = MapAppService(map_service)

    window = MainWindow(app_map_service)
    window.show()

    app.exec()
