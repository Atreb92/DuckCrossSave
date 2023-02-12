import json
import os
import sys
from utils import resource_path

class Config:
    def __init__(self, game):
        self.game = game.lower()
        self.game_config = None
        self.load_config()
        self.default_location = None

    def load_config(self):
        with open("config.json") as f:
            config = json.load(f)
        self.game_config = [x for x in config["games"] if self.game in x["name"]][0]

    def get_location_by_os(self, operating_system):
        self.default_location = os.path.expandvars(self.game_config["default_locations"][operating_system])
    def get_backup_folder(self, cur_time, operating_system, game):
        return resource_path(f"backup/{cur_time}/{operating_system}/{game}")
