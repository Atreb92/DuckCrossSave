import sys
import ftpdcs

from config import Config
import datetime
from steam import backup_local_saves

from comparer import Comparer



game = "Stardew Valley"

def main():
    cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    config = Config(cur_time, game)

    #Backup steam saves
    steam_backup_folder = config.get_backup_folder("steam", game)
    steam_path = config.get_location_by_os("steam")
    backup_local_saves(steam_path, steam_backup_folder)

    #Backup switch saves
    ftp = ftpdcs.FTPDCS("secrets")
    backup_folder = config.get_backup_folder("switch", game)
    switch_path = config.get_location_by_os("switch")
    ftp.backup_directory(switch_path, backup_folder)

    comparer = Comparer(config)
    out_dict = comparer.compare_platforms(["steam", "test"], compare_type="int")
    print(out_dict)

if __name__ == "__main__":
    sys.exit(main())