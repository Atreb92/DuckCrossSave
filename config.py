import json
import os
import sys
from distutils.dir_util import copy_tree
from utils import resource_path
import datetime
class Config:
    def __init__(self, game, os):
        self.game = game.lower()
        self.os = os.lower()
        self.default_location = None
        self.load_config()
        print(self.default_location)

    def load_config(self):
        with open("config.json") as f:
            config = json.load(f)
        game_config = [x for x in config["games"] if self.game in x["name"]][0]
        self.default_location = os.path.expandvars(game_config["default_locations"][self.os])
    def backup_saves(self):
        cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        copy_tree(self.default_location, resource_path(f"backup/{self.os}/{self.game}_{cur_time}"))

def main():
    config = Config("Stardew Valley", "steam")
    config.backup_saves()


if __name__ == "__main__":
    sys.exit(main())