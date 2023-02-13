import json
import os
from utils import resource_path

class Config:
    def __init__(self, cur_time, game):
        self.cur_time = cur_time
        self.game = game.lower()
        self.game_config = None
        self.load_config()
        # self.default_location = None

    def load_config(self):
        with open("config.json") as f:
            config = json.load(f)
        self.game_config = [x for x in config["games"] if self.game in x["name"]][0]

    def get_location_by_os(self, platform):
        return os.path.expandvars(self.game_config["default_locations"][platform])
    
    def get_backup_folder(self, platform, game):
        return resource_path(f"backup/{self.cur_time}/{platform}/{game}")

    def get_node(self):
        return self.game_config["node"]
