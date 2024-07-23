import os
import shutil
import globals
import threading
from datetime import datetime

from functools import partial
from sys import platform
import ui

class AppInitializer:
    def check_platform():
        # global currDrive, available_drives
        if platform == "win32":
            globals.available_drives = [
                chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")
            ]  # 65-91 -> search for drives A-Z
            globals.currDrive = globals.available_drives[0]  # current selected drive
        elif platform == "linux":
            globals.available_drives = "/"
            globals.currDrive = globals.available_drives

    def read_theme():
        # global theme, file_path
        with open(globals.file_path + "../res/theme.txt") as f:  # closes file automatically
            globals.theme = f.readline()
            if (globals.theme == globals.literaL or globals.theme == globals.mintyL 
                or globals.theme == globals.morphL or globals.theme == globals.yetiL):
                globals.theme_mode = "light"
            else:
                globals.theme_mode = "dark"
        if globals.theme == "":  # if theme.txt is empty, set default theme
            globals.theme = globals.literaL
            globals.theme_mode = "light"

    def read_font():
        #global font_size
        with open(globals.file_path + "../res/font.txt") as f:  # closes file automatically
            globals.font_size = f.readline()
        if globals.font_size == "":  # if font.txt is empty, set default font
            globals.font_size = 10

    def __init__(self):
        AppInitializer.check_platform()
        AppInitializer.read_theme()
        AppInitializer.read_font()

class SettingManager:
    def write_theme(theme):
        with open(
            globals.file_path + "../res/theme.txt", "w"
        ) as f:  # closes file automatically
            f.write(theme)
        ui.warning_popup()


    def change_scale(multiplier, s):
        scale = round(multiplier * 28)  # 28 is default
        s.configure("Treeview", rowheight=scale)

    def change_font_size(size):
        with open(
            globals.file_path + "../res/font.txt", "w"
        ) as f:  # closes file automatically
            f.write(str(size))

    

class UIManager:
    def focus_out(searchEntry, window, event):
        searchEntry.delete(0, "end")
        searchEntry.insert(0, "Search files..")
        window.focus()

    def change_font_popup(size):
        ui.warning_popup()
        SettingManager.change_font_size(size)


class OnClick:
    def click(searchEntry, event):
        if searchEntry.get() == "Search files..":
            searchEntry.delete(0, "end")

    def on_right_click(m, event):
        EventHandler.select_item(event)
        m.tk_popup(event.x_root, event.y_root)

    def on_double_click(event=None):
        #global items
        iid = globals.items.focus()
        # iid = items.identify_row(event.y) # old
        if iid == "":  # if double click on blank, don't do anything
            return
        for item in globals.items.selection():
            tempDictionary = globals.items.item(item)
            tempName = tempDictionary["values"][0]  # get first value of dictionary
        try:
            newPath = os.getcwd() + "/" + tempName
            if os.path.isdir(
                newPath
            ):  # if file is directory, open directory else open file
                os.chdir(newPath)
            else:
                os.startfile(newPath)
            ui.refresh([])
        except Exception as e:
            print(e)
            newPath = newPath.replace(tempName, "")
            os.chdir("../")

class FileOperation:
    def del_file():
        if os.path.isfile(os.getcwd() + "/" + globals.selectedItem):
            os.remove(os.getcwd() + "/" + globals.selectedItem)
        elif os.path.isdir(os.getcwd() + "/" + globals.selectedItem):
            # os.rmdir(os.getcwd() + "/" + selectedItem)
            shutil.rmtree(os.getcwd() + "/" + globals.selectedItem)


    def copy():
        #global src, items
        if globals.items.focus() != "":  # if there is a focused item
            globals.src = os.getcwd() + "/" + globals.selectedItem


    def paste():
        #global src
        dest = os.getcwd() + "/"
        if not os.path.isdir(globals.src) and globals.src != "":
            try:
                t1 = threading.Thread(
                    target=shutil.copy2, args=(globals.src, dest)
                )  # use threads so gui does not hang on large file copy
                t2 = threading.Thread(target=ui.paste_popup, args=([t1]))
                t1.start()
                t2.start()
            except Exception as e:
                print(e)
                pass
        elif os.path.isdir(globals.src) and globals.src != "":
            try:
                new_dest_dir = os.path.join(dest, os.path.basename(globals.src))
                os.makedirs(new_dest_dir)
                t1 = threading.Thread(  # use threads so gui does not hang on large directory copy
                    target=shutil.copytree,
                    args=(globals.src, new_dest_dir, False, None, shutil.copy2, False, True),
                )
                t2 = threading.Thread(target=ui.paste_popup, args=([t1]))
                t1.start()
                t2.start()
            except Exception as e:
                print(e)
                pass

    def search(searchEntry, event):
        fileNames = os.listdir()
        query = searchEntry.get()  # get query from text box
        query = query.lower()
        queryNames = []

        for name in fileNames:
            if name.lower().find(query) != -1:  # if query in name
                queryNames.append(name)
        ui.refresh(queryNames)

    def previous():
        #global lastDirectory
        globals.lastDirectory = os.getcwd()
        os.chdir("../")
        ui.refresh([])

    def next():
        try:
            os.chdir(globals.lastDirectory)
            ui.refresh([])
        except Exception as e:
            print(e)
            return
    
    def cd_drive(drive, queryNames):
        #global fileNames, currDrive, cwdLabel
        globals.cwdLabel.config(text=" " + drive)
        globals.currDrive = drive
        globals.fileNames = os.listdir(globals.currDrive)
        os.chdir(globals.currDrive + "/")
        ui.refresh(queryNames)

class Sorter:
    def sort_key_dates(item):
        return datetime.strptime(item[0], "%d-%m-%Y %I:%M")

    def sort_key_size(item):
        num_size = item[0].split(" ")[0]
        if num_size != "":
            return int(num_size)
        else:
            return -1  # if it's a directory, give it negative size value, for sorting
        
    def sort_col(col, reverse):
        #global items
        l = [(globals.items.set(k, col), k) for k in globals.items.get_children("")]
        if col == "Name" or col == "Type":
            l.sort(reverse=reverse)
        elif col == "Date modified":
            l = sorted(l, key=Sorter.sort_key_dates, reverse=reverse)
        elif col == "Size":
            l = sorted(l, key=Sorter.sort_key_size, reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            globals.items.move(k, "", index)

        # reverse sort next time
        globals.items.heading(col, command=partial(Sorter.sort_col, col, not reverse))

class EventHandler:
    def select_item(event):
        #global selectedItem, items
        # selectedItemID = items.focus()
        iid = globals.items.identify_row(event.y)
        if iid:
            globals.items.selection_set(iid)
            globals.selectedItem = globals.items.item(iid)["values"][0]
            print(globals.selectedItem)
            globals.items.focus(iid)  # Give focus to iid
        else:
            pass
    
    def up_key(event):
        #global selectedItem, items
        iid = globals.items.focus()
        iid = globals.items.prev(iid)
        if iid:
            globals.items.selection_set(iid)
            globals.selectedItem = globals.items.item(iid)["values"][0]
            print(globals.selectedItem)
        else:
            pass

    def down_key(event):
        #global selectedItem, items
        iid = globals.items.focus()
        iid = globals.items.next(iid)
        if iid:
            globals.items.selection_set(iid)
            globals.selectedItem = globals.items.item(iid)["values"][0]
            print(globals.selectedItem)
        else:
            pass