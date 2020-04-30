from abc import ABC, abstractmethod


class RespiMode(ABC):
    peep = 0

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def process_trigger(self):
        pass

    @abstractmethod
    def get_dict(self):
        pass
