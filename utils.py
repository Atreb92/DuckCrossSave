import sys, os, glob, codecs
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_latest(path, filetype="*"):
    list_of_files = glob.glob(f'{path}/{filetype}') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def open_file(path, mode='r'):
    if 'r' in mode:
        if os.path.isfile(path):
            f = open(path, 'rb')
            header = f.read(4)
            f.close()
            encodings = [ (codecs.BOM_UTF32, 'utf-32'), (codecs.BOM_UTF16, 'uft-16'), (codecs.BOM_UTF8, 'uft-8-sig')]
            for h, e in encodings:
                if header.find(h) == 0:
                    encoding = e
                    break
        return codecs.open(path, mode, encoding)