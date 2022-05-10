from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QComboBox, QPushButton
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
from app_services.map_app_service import MapAppService
from services.ya_map_service import YaMapService
from domain.request import Request


class MainWindow(QWidget):
    def __init__(self, app_service: MapAppService, parent=None):
        super().__init__(parent)
        self.app_service = app_service
        self.request = Request('map')
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 800)
        self.map_label = QLabel(self)
        self.map_box = QComboBox(self)
        self.map_box.addItems(['map'] + list(set(['sat', 'skl'])))
        self.pushbutton = QPushButton(self)
        self.pushbutton.setText('Изменить')
        self.pushbutton.clicked.connect(self.click)

        layout = QVBoxLayout(self)
        layout.addWidget(self.map_box)
        layout.addWidget(self.pushbutton)
        layout.addWidget(self.map_label)

        self.setLayout(layout)
        self.show_map()

    def click(self):
        self.request = Request(self.map_box.currentText())
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
