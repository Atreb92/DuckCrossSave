import sys
import ftpdcs

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
    steam_path = config.get_location_by_os(operating_system)
    backup_local_saves(steam_path, backup_folder)

    #Backup switch saves
    ftp = ftpdcs.FTPDCS("secrets")
    backup_folder = config.get_backup_folder(cur_time, "switch", game)
    switch_path = config.get_location_by_os("switch")
    ftp.backup_directory(switch_path, backup_folder)

if __name__ == "__main__":
    sys.exit(main())