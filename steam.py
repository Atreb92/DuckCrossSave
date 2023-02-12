from distutils.dir_util import copy_tree


def backup_local_saves(location, backup_folder):
    copy_tree(location, backup_folder)
