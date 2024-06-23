import ttkbootstrap as ttk
import tkinter as tk

fileNames = []
file_path = ""  # path of main.py
lastDirectory = ""
selectedItem = ""  # focused item on Treeview
src = ""  # temp path for copying
theme = ""  # current theme
theme_mode = "" # light or dark
photo_ref = []  # keeps references of photos
currDrive = ""
available_drives = []
font_size = "10"  # default is 10
items: ttk.Treeview  # holds treeview items
cwdLabel: ttk.Label
footer: ttk.Label

# file icons
folderIcon: list
fileIcon: list
backIcon: list
frontIcon: list
copyIcon: list
cpuIcon: list
deleteIcon: list
driveIcon: list
fontIcon: list
appIcon: list
infoIcon: list
memoryIcon: list
networkIcon: list
pasteIcon: list
pieIcon: list
processIcon: list
reloadIcon: list
renameIcon: list
scaleIcon: list
themesIcon: list
exitIcon: list

# available themes
# Dark
solarD = "solar"
superheroD = "superhero"
Darkly = "darkly"
CyborgD = "cyborg"
VaporD = "vapor"
# Light
literaL = "litera"  # default theme
mintyL = "minty"
morphL = "morph"
yetiL = "yeti"
