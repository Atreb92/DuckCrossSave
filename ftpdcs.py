import ftputil
from ftplib import FTP
from ftputil.error import PermanentError
import re
import json
import traceback
from datetime import datetime
import os
from utils import resource_path

class SaveFileNotFoundError(Exception):
    pass

class FTPDCS:
    def __init__(self, credential_filename):
        self.open_connection(credential_filename)

    def __load_credentials(self, filename):
        try:
            with open(resource_path(filename), mode="r", encoding="utf-8") as inFile:
                dictFile = json.load(inFile)
                
                return dictFile["username"], dictFile["password"], dictFile["address"], dictFile["port"]
        except FileNotFoundError:
            print(f"File not found: {filename}")

    def open_connection(self, credential_filename):
        username, password, address, port = self.__load_credentials(credential_filename)

        try:
            session_factory = ftputil.session.session_factory(
                base_class = FTP,
                port = 5000
            )
            self.ftp = ftputil.FTPHost(address, username, password, session_factory=session_factory)

        except ConnectionRefusedError:
            print("Impossible to connect to target")
        except:
            traceback.print_exc()

    def backup_directory(self, game_path, path):
        try:
            self.ftp.chdir(f"{game_path}")
            
            most_recent_datetime = None
            most_recent_directory = None

            for directory in self.ftp.listdir(self.ftp.getcwd()):
                if re.match(r"^(?!AUTO\s).*(\s-\s\d{4}\.\d{2}\.\d{2}\s@\s\d{2}\.\d{2}\.\d{2}){1}$", directory):
                    folder_datetime = datetime.strptime(directory.split(" - ")[-1], f"%Y.%m.%d @ %H.%M.%S")
                    
                    if (most_recent_datetime == None) or (most_recent_datetime < folder_datetime):
                        most_recent_datetime = folder_datetime
                        most_recent_directory = directory
            
            if not most_recent_directory:
                raise SaveFileNotFoundError
            
            else:
                os.makedirs(resource_path(f"{path}"))
                self.__recursive_download(f"{game_path}/{most_recent_directory}", resource_path(f"{path}"))

        except PermanentError:
            print(f"Game directory {game_path} not found: {game_path}")
        except:
            traceback.print_exc()

    def __recursive_download(self, source, destination):
        self.ftp.chdir(source)
        for root, dirs, filenames in self.ftp.walk(source):
            for dir in dirs:
                os.mkdir(resource_path(f"{root.replace(source, destination)}/{dir}"))
            
            for f in filenames:
                self.ftp.download(f"{root}/{f}", f"{root.replace(source, destination)}/{f}")

    
