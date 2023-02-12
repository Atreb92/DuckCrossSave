import codecs
import os
from utils import get_latest, open_file


class Config:
    def __init__(self, path):
        self.save_file = None
        self.load_config(path)
        pass
    def load_config(self, path):
        if os.path.isfile(path):
            self.__load_config_manual(path)
        else:
            self.__load_config_automatic(path)

    def __load_config_manual(self, path):
        self.save_file = open_file(path)

    def __load_config_automatic(self, path):
        latest_file = get_latest(path)
        self.save_file = open_file(latest_file)


