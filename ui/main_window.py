from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap
from app_services.map_app_service import MapAppService
from services.ya_map_service import YaMapService


class MainWindow(QWidget):
    def __init__(self, app_service: MapAppService, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 800)
        self.map_label = QLabel(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.map_label)

        self.setLayout(layout)

    def show_map(self):
        map = self.app_service.execute(self.request)

        pixmap = QPixmap()
        pixmap.loadFromData(map, 'PNG')
        self.map_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication([])

    map_service = YaMapService()
    add_map_service = MapAppService(map_service)

    window = MainWindow()
    window.show()

    app.exec()