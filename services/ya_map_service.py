from domain.request import Request
from services.i_map_service import IMapService
import requests


class YaMapService(IMapService):
    url = "http://static-maps.yandex.ru/1.x/"

    def get_map(self, req:Request):
        return requests.get(self.url, params={'ll': str(req.get_longitude()) + ',' + str(req.get_latitude()),
                                              'z': req.get_zoom(),
                                              'l': req.get_l(),
                                              'pt': req.get_sp_top()}).content
