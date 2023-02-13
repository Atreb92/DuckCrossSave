import os
import traceback
import lxml.etree
from utils import resource_path
from deepdiff import DeepDiff


class Comparer:
    def __init__(self, config):
        self.config = config

    def compare_platforms(self, platforms, compare_type="int"):
        saves_dict = self.get_save_files(platforms)
        saves_node_info = self.get_saves_node_info(platforms, saves_dict)
        out_dict = {x:[] for x in platforms}
        return self.compare_int(out_dict, platforms, saves_node_info)

    def compare_int(self, out_dict, platforms, saves_node_info):
        for key in saves_node_info[platforms[0]].keys() & saves_node_info[platforms[1]].keys():
            if int(saves_node_info[platforms[0]][key]) > int(saves_node_info[platforms[1]][key]):
                out_dict[platforms[0]].append(key)
            elif int(saves_node_info[platforms[0]][key]) < int(saves_node_info[platforms[1]][key]):
                out_dict[platforms[1]].append(key)
        return out_dict

    def get_saves_node_info(self, platforms, saves_dict):
        saves_node_info = {x: {} for x in saves_dict.keys()}
        for platform in platforms:
            for save in saves_dict[platform]:
                save_file_path = os.path.join(self.config.get_backup_folder(platform, self.config.game), save, save)
                try:
                    saves_node_info[platform][save] = extract_playtime_from_xml(save_file_path, self.config.get_node())
                except FileNotFoundError:
                    saves_node_info[platform][save] = "0"
        return saves_node_info

    def get_save_files(self, platforms):
        saves_dict = {}
        for platform in platforms:
            saves_dict[platform] = self.get_platform_save_data(self.config.get_backup_folder(platform, self.config.game))
        return saves_dict

    def get_platform_save_data(self, path):
        save_list = []
        for dir in os.listdir(path):
            if os.path.isdir(f"{path}/{dir}"):
                if dir not in save_list:
                    save_list.append(dir)
        return save_list

def extract_playtime_from_xml(path, node):
    save1 = open(path, "r", encoding="utf-8")
    root = lxml.etree.fromstring(save1.read())
    textelem = root.find(node)
    return textelem.text


