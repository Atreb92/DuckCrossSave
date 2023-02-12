import sys

from config import Config
import datetime
from steam import backup_local_saves


game = "Stardew Valley"

def main():
    cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    operating_system = "steam"

    config = Config(game)
    backup_folder = config.get_backup_folder(cur_time, operating_system, game)

    #Backup steam saves
    config.get_location_by_os(operating_system)
    backup_local_saves(config.default_location, backup_folder)
"""
    #Backup switch saves
    ftp = ftpdcs.FTPDCS("secrets")
    backup_folder = config.get_backup_folder(cur_time, "switch", game)
    ftp.backup_directory(game, backup_folder)
"""
if __name__ == "__main__":
    sys.exit(main())