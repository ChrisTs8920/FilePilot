import ttkbootstrap as ttk
import tkinter as tk

fileNames = []
file_path = ""  # path of main.py
lastDirectory = ""
selectedItem = ""  # focused item on Treeview
src = ""  # temp path for copying
theme = ""  # current theme
photo_ref = []  # keeps references of photos
currDrive = ""
available_drives = []
font_size = "10"  # default is 10
folderIcon: tk.PhotoImage
fileIcon: tk.PhotoImage
items: ttk.Treeview  # holds treeview items
cwdLabel: ttk.Label
footer: ttk.Label

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
