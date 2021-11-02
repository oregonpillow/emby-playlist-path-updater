# emby-playlist-path-updater
Script to mass update playlist xml paths for Emby/Jellyfin. Creates a backup of current playlist folder before modifying original.


```python
import os
from os.path import join
import shutil

"""
Update the paths in your emby playlists folder.
Creates a backup before modifying.
Tested on python 3.9.7.


Requirements to run:
	Update playlist_pth --> path of your emby playlists folder
	Update path_dic     --> map your old paths:new paths


"""
playlist_pth = '<my/path/playlists>'

path_dic   = {
	'<old path1>'          : '<new path1>',
	'<old path2>'          : '<new path2>',
	'<old path3>'          : '<new path3>',
	'<old path4>'          : '<new path4>'
	}
	





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
print("Playlist paths updated --> " + playlist_pth)
```
