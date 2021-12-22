import os
from os.path import join
import shutil
import xml.etree.ElementTree as ET

"""
Update the paths in your emby playlists folder.

"""
playlist_pth = '/mnt/USBStorage/dockers/emby/emby_config/config/data/playlists'




playlists_lst = []
for root, dirs, files in os.walk(playlist_pth):
        for file in files:
                if file.endswith(".xml"):
                        xml_pth = join(root, file)
                        playlists_lst.append(xml_pth)


if len(playlists_lst) > 0:
        print("===== Playlists found =====\n")
        for playlist in playlists_lst:
                print(playlist)
        print("\n===========================\n")
else:
        print("*** NO PLAYLISTS FOUND ***")
        exit()

backup_pth = playlist_pth.replace('playlists','playlists_backup')
if os.path.isdir(backup_pth):
        print("*** {} ALREADY EXISTS ***".format(backup_pth))
        print("No files modified")
        exit()

backup = shutil.copytree(playlist_pth, backup_pth)
print("Playlist backed up     --> " + backup)
print("Updating playlists...")

path_dic   = {}
for pth in playlists_lst:
        root = ET.parse(pth).getroot()
        items = root.findall('PlaylistItems/PlaylistItem/Path')
        for item in items:
                path = item.text.replace('media','mnt')
                split = os.path.split(os.path.abspath(path))
                path_dir = split[0]
                path_fil = split[1]
                for filename in os.listdir(path_dir):
                        if filename.endswith(".mkv") or filename.endswith(".mp4"):
                                correct_pth = os.path.join(path_dir, filename).replace('mnt','media')
                                wrong_pth = os.path.join(path_dir, path_fil).replace('mnt','media')
                                path_dic[wrong_pth] = correct_pth





for pth in playlists_lst:
        for old_pth in path_dic:
                        new_pth = path_dic[old_pth]
                        fin = open(pth, "rt")
                        data = fin.read()
                        updated_data = data.replace(old_pth,new_pth)
                        fin.close()
                        fin = open(pth,"wt")
                        fin.write(updated_data)
                        fin.close

print("Complete.")
