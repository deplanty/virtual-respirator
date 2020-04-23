from abc import ABC, abstractmethod


class FrameMode(ABC):
    @abstractmethod
    def set_default(self):
        pass

    @abstractmethod
    def get(self):
        pass
