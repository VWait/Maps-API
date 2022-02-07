from abc import ABC, abstractmethod

from domain.request import Request


class IMapService(ABC):
    @abstractmethod
    def get_map(self, request:Request):
        pass
