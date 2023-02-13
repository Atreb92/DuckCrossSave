import os
import traceback
import lxml.etree
from utils import resource_path

def stardew_valley(cur_time, platform1, platform2):
    try:
        platform1_path = resource_path(f"backup/{cur_time}/{platform1}/Stardew Valley")
        platform2_path = resource_path(f"backup/{cur_time}/{platform2}/Stardew Valley")
        
        save_list = []

        get_save_list(platform1_path, save_list)
        get_save_list(platform2_path, save_list)

        out_dict = {
            platform1: [],
            platform2: []
        }
        for save in save_list:
            try:
                save1_playtime = int(extract_playtime_from_xml(f"{platform1_path}/{save}/{save}", 'player/millisecondsPlayed'))
            except FileNotFoundError:
                out_dict[platform2].append(save)
                continue
            try:
                save2_playtime = int(extract_playtime_from_xml(f"{platform2_path}/{save}/{save}", 'player/millisecondsPlayed'))
            except FileNotFoundError:
                out_dict[platform1].append(save)
                continue
            
            if save1_playtime > save2_playtime:
                out_dict[platform1].append(save)
            elif save1_playtime < save2_playtime:
                out_dict[platform2].append(save)
            

        return out_dict
        #return [["switch", "paperopoli", "a", "b"],["steam", "cotton", "c"]]
    except FileNotFoundError as e:
        print(f"Directory not found: {e}")
    except:
        traceback.print_exc()

def extract_playtime_from_xml(path, node):
    save1 = open(path, "r", encoding="utf-8")
    root = lxml.etree.fromstring(save1.read())
    textelem = root.find(node)
    return textelem.text

def get_save_list(path, save_list):
    for dir in os.listdir(path):
        if os.path.isdir(f"{path}/{dir}"):
            if dir not in save_list:
                save_list.append(dir)