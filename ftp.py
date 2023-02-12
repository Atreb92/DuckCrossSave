import ftputil
from ftplib import FTP
import json
import traceback
from utils import resource_path

def __loadCredentials(filename):
    try:
        with open(resource_path(filename), mode="r", encoding="utf-8") as inFile:
            dictFile = json.load(inFile)
            
            return dictFile["username"], dictFile["password"], dictFile["address"], dictFile["port"]
    except FileNotFoundError:
        print(f"File not found: {filename}")

def openConnection(credential_filename):
    username, password, address, port = __loadCredentials(credential_filename)

    try:
        session_factory = ftputil.session.session_factory(
            base_class = FTP,
            port = 5000
        )
        ftp = ftputil.FTPHost(address, username, password, session_factory=session_factory)
        return ftp
    except ConnectionRefusedError:
        print("Impossible to connect to target")
    except:
        print(traceback.print_exc())

ftp_switch = openConnection("secrets")

print(ftp_switch.listdir(ftp_switch.getcwd()))
#ftp_switch.listdir(ftp_switch.curdir)