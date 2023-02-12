from ftplib import FTP
import json
import traceback

def __loadCredentials(filename):
    try:
        with open(filename, mode="r", encoding="utf-8") as inFile:
            dictFile = json.load(inFile)
            
            return dictFile["username"], dictFile["password"], dictFile["address"], dictFile["port"]
    except FileNotFoundError:
        print(f"File not found: {filename}")

def openConnection(credential_filename):
    username, password, address, port = __loadCredentials(credential_filename)

    try:
        ftp = FTP()
        ftp.connect(address, port)
        ftp.login(user=username, passwd=password)

        return ftp 
    except ConnectionRefusedError:
        print("Impossible to connect to target")
    except:
        print(traceback.print_exc())

ftp_switch = openConnection("secrets")
