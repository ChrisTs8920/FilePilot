import os
import tkinter as tk
from datetime import datetime

# from tkinter import ttk
from functools import partial
from sys import platform
import shutil

# from PIL import Image, ImageTk

import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.dialogs.dialogs import Querybox

import ext

# TODO:
# Linux compatibility,
# Add scaling,
# grab file icons from files (Or pillow library),
# improve extension handling,
# break into modules,
# editable path,
# column sorting,
# code improvements, refactoring

# globals
fileNames = []
file_path = ""  # path of main.py
lastDirectory = ""
selectedItem = ""  # focused item on Treeview
fileSizesSum = 0  # total file size of current directory

if platform == "win32":
    available_drives = [
        chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")
    ]  # 65-91 -> search for drives A-Z
    currDrive = available_drives[0]  # current selected drive
elif platform == "linux":
    available_drives = "/"
    currDrive = available_drives

# current theme
theme = ""
# available themes
# Dark
solarD = "solar"
superheroD = "superhero"
Darkly = "darkly"
CyborgD = "cyborg"
VaporD = "vapor"
# Light
literaL = "litera"
mintyL = "minty"
morphL = "morph"
yetiL = "yeti"

# scales
s100 = 28  # 100% scale


def createWindow():
    # root = tk.Tk()
    root = ttk.Window(themename=theme)
    root.title("My File Explorer")
    root.geometry("1280x720")
    root.resizable(True, True)
    root.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))
    return root


def refresh(cwdLabel, items, folderIcon, fileIcon, footer, queryNames):
    global fileNames
    # Refresh Header
    cwdLabel.config(text=" " + os.getcwd())
    # --Refresh Header

    # Refresh Browse
    fileSizesSum = 0
    if queryNames:  # if user gave query and pressed enter
        fileNames = queryNames
    else:
        fileNames = os.listdir(os.getcwd())
    fileTypes = [None] * len(fileNames)
    fileSizes = [None] * len(fileNames)
    fileDateModified = []
    for i in items.get_children():  # delete data from previous directory
        items.delete(i)
    for i in range(len(fileNames)):
        try:
            # modification time of file
            fileDateModified.append(
                datetime.fromtimestamp(os.path.getmtime(fileNames[i])).strftime(
                    "%d-%m-%Y %I:%M"
                )
            )
            # size of file
            fileSizes[i] = str(
                round(os.stat(fileNames[i]).st_size / 1024)
            )  # str->round->size of file in KB
            fileSizesSum += int(fileSizes[i])
            fileSizes[i] = str(round(os.stat(fileNames[i]).st_size / 1024)) + " KB"
            # check file type
            ext.extensions(fileTypes, fileNames, i)

            # insert
            if fileTypes[i] == "Directory":
                items.insert(
                    parent="",
                    index=i,
                    values=(fileNames[i], fileDateModified[i], fileTypes[i], ""),
                    image=folderIcon,
                )
            else:
                items.insert(
                    parent="",
                    index=i,
                    values=(
                        fileNames[i],
                        fileDateModified[i],
                        fileTypes[i],
                        fileSizes[i],
                    ),
                    image=fileIcon,
                )
        except:
            pass
        # --Refresh Browse

    # Draw browse
    items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # --Draw browse

    # Refresh Footer
    footer.config(
        text=" "
        + str(len(fileNames))
        + " items | "
        + str(round(fileSizesSum / 1024, 1))
        + " MB Total"
    )
    footer.pack(fill=tk.BOTH)
    # --Refresh Footer


def previous(cwdLabel, items, folderIcon, fileIcon, footer):
    global lastDirectory
    lastDirectory = os.getcwd()
    os.chdir("../")
    refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])


def next(cwdLabel, items, folderIcon, fileIcon, footer):
    try:
        os.chdir(lastDirectory)
        refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])
    except:
        return


# open file
def onDoubleClick(cwdLabel, items, folderIcon, fileIcon, footer, event):
    iid = items.identify_row(event.y)
    if iid == "":  # if double click on blank, don't do anything
        return
    for item in items.selection():
        tempDictionary = items.item(item)
        tempName = tempDictionary["values"][0]  # get first value of dictionary
    try:
        newPath = os.getcwd() + "/" + tempName
        if os.path.isdir(
            newPath
        ):  # if file is directory, open directory else open file
            os.chdir(newPath)
        else:
            os.startfile(newPath)
        refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])
    except:
        newPath = newPath.replace(tempName, "")
        os.chdir("../")
        pass


def onRightClick(m, items, event):
    iid = items.identify_row(event.y)
    if iid:
        items.selection_set(iid)
        global selectedItem
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


def search(searchEntry, cwdLabel, items, folderIcon, fileIcon, footer, event):
    fileNames = os.listdir()
    query = searchEntry.get()  # get query from text box
    query = query.lower()
    queryNames = []

    for name in fileNames:
        if name.lower().find(query) != -1:  # if query in name
            queryNames.append(name)
    refresh(cwdLabel, items, folderIcon, fileIcon, footer, queryNames)


def create_widgets(window):
    s = ttk.Style()
    # Browse Frame
    browseFrame = ttk.Frame(window)
    scroll = ttk.Scrollbar(browseFrame, orient="vertical")
    items = ttk.Treeview(
        browseFrame,
        columns=("Name", "Date modified", "Type", "Size"),
        yscrollcommand=scroll.set,
        height=15,
        style="Custom.Treeview",
    )
    scroll.config(command=items.yview)  # scroll with mouse drag
    # --Browse Frame

    # Footer Frame
    footerFrame = ttk.Frame(window)
    footer = ttk.Label(footerFrame)
    grip = ttk.Sizegrip(footerFrame, bootstyle="default")
    # --Footer Frame

    folderIcon = tk.PhotoImage(file=file_path + "Folder-icon.png", width=20, height=16)
    fileIcon = tk.PhotoImage(file=file_path + "File-icon.png", width=20, height=16)

    # Header Frame
    refreshIcon = tk.PhotoImage(file=file_path + "Very-Basic-Reload-icon.png")
    backArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Back-icon.png")
    frontArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Front-icon.png")
    headerFrame = ttk.Frame()
    cwdLabel = ttk.Label(
        headerFrame,
        text=" " + os.getcwd(),
        relief="flat",
        width=110,
    )
    searchEntry = ttk.Entry(headerFrame, width=30)
    searchEntry.insert(0, "Search files..")
    searchEntry.bind("<Button-1>", partial(click, searchEntry))
    searchEntry.bind("<FocusOut>", partial(FocusOut, searchEntry, window))
    backButton = ttk.Button(
        headerFrame,
        image=backArrowIcon,
        command=partial(previous, cwdLabel, items, folderIcon, fileIcon, footer),
        bootstyle="light",
    )
    forwardButton = ttk.Button(
        headerFrame,
        image=frontArrowIcon,
        command=partial(next, cwdLabel, items, folderIcon, fileIcon, footer),
        bootstyle="light",
    )
    refreshButton = ttk.Button(
        headerFrame,
        command=partial(refresh, cwdLabel, items, folderIcon, fileIcon, footer, []),
        image=refreshIcon,
        bootstyle="light",
    )

    # tooltips for buttons
    ToolTip(backButton, text="Back", bootstyle=("default", "inverse"))
    ToolTip(forwardButton, text="Forward", bootstyle=("default", "inverse"))
    ToolTip(refreshButton, text="Refresh", bootstyle=("default", "inverse"))
    # keep references for buttons
    backButton.img_reference = backArrowIcon
    forwardButton.img_reference = frontArrowIcon
    refreshButton.img_reference = refreshIcon
    # --Header Frame

    # Right click menu
    m = ttk.Menu(window, tearoff=False, font=("TkDefaultFont", 10))
    # m.add_command(label="Cut")
    # m.add_command(label="Copy")
    # m.add_command(label="Paste")
    """m.add_command(
        label="Open",
        command=partial(
            onDoubleClick, cwdLabel, items, folderIcon, fileIcon, footer
        ),
    )"""
    # m.add_separator()
    m.add_command(label="New file", command=partial(new_file_popup))
    m.add_command(label="Rename selected", command=partial(rename_popup, items))
    m.add_command(label="Delete selected", command=partial(del_file_popup, items))
    m.add_separator()
    m.add_command(
        label="Refresh",
        command=partial(refresh, cwdLabel, items, folderIcon, fileIcon, footer, []),
    )
    # --Right click menu

    s.configure(".", font=("TkDefaultFont", 10))  # set font size
    s.configure("Treeview", rowheight=28)  # customize treeview
    s.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # remove borders

    items.column("#0", width=40, stretch=tk.NO)
    items.column("Name", anchor=tk.W, width=150, minwidth=120)
    items.column("Date modified", anchor=tk.CENTER, width=200, minwidth=120)
    items.column("Size", anchor=tk.CENTER, width=80, minwidth=60)
    items.column("Type", anchor=tk.CENTER, width=120, minwidth=60)
    items.heading("Name", text="Name", anchor=tk.CENTER)
    items.heading("Date modified", text="Date modified", anchor=tk.CENTER)
    items.heading("Type", text="Type", anchor=tk.CENTER)
    items.heading("Size", text="Size", anchor=tk.CENTER)
    items.bind(
        "<Double-1>",
        partial(onDoubleClick, cwdLabel, items, folderIcon, fileIcon, footer),
    )  # command on double click
    items.bind("<ButtonRelease-1>", partial(selectItem, items))
    items.bind("<Button-3>", partial(onRightClick, m, items))  # command on right click
    items.bind("<Up>", partial(up_key, items))  # bind up arrow key
    items.bind("<Down>", partial(down_key, items))  # bind down arrow key
    # --Browse Frame

    # Menu bar
    bar = ttk.Menu(window, font=("TkDefaultFont", 10))
    window.config(menu=bar)

    # image = Image.open(file_path + "icon.png")
    # photo = ImageTk.PhotoImage(image)

    file_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))
    # ile_menu.img_reference = photo  # keep img reference
    file_menu.add_command(
        label="New file",
        # image=photo,
        # compound="left",
        command=new_file_popup,
    )
    file_menu.add_command(label="Rename selected", command=partial(rename_popup, items))
    file_menu.add_command(
        label="Delete selected", command=partial(del_file_popup, items)
    )
    # file_menu.add_command(label="Create directory", command=new_dir)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.destroy)

    drives_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))
    for drive in available_drives:
        drives_menu.add_command(
            label=drive,
            command=partial(
                cd_drive, drive, cwdLabel, items, folderIcon, fileIcon, footer, []
            ),
        )

    stats_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))
    stats_menu.add_command(
        label="Drive Capacities", command=partial(drive_stats, window)
    )

    preferences_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))

    sub_themes = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))
    sub_themes.add_command(label="Darkly", command=partial(write_theme, Darkly))
    sub_themes.add_command(label="Solar Dark", command=partial(write_theme, solarD))
    sub_themes.add_command(
        label="Superhero Dark", command=partial(write_theme, superheroD)
    )
    sub_themes.add_command(label="Cyborg Dark", command=partial(write_theme, CyborgD))
    sub_themes.add_command(label="Vapor Dark", command=partial(write_theme, VaporD))
    sub_themes.add_separator()
    sub_themes.add_command(label="Litera Light", command=partial(write_theme, literaL))
    sub_themes.add_command(label="Minty Light", command=partial(write_theme, mintyL))
    sub_themes.add_command(label="Morph Light", command=partial(write_theme, morphL))
    sub_themes.add_command(label="Yeti Light", command=partial(write_theme, yetiL))
    preferences_menu.add_cascade(label="Themes", menu=sub_themes)

    about_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", 10))
    about_menu.add_command(
        label="About the app",
        command=about_popup,
    )

    bar.add_cascade(label="File", menu=file_menu, underline=0)
    bar.add_cascade(label="Select drive", menu=drives_menu, underline=0)
    bar.add_cascade(label="Stats", menu=stats_menu, underline=0)
    bar.add_cascade(label="Preferences", menu=preferences_menu, underline=0)
    bar.add_cascade(label="About", menu=about_menu, underline=0)
    # --Menu bar

    # packs
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    backButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    forwardButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    cwdLabel.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH, expand=True)
    refreshButton.pack(side=tk.LEFT, padx=1, pady=10, fill=tk.BOTH)
    searchEntry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    grip.pack(side=tk.RIGHT, fill=tk.BOTH, padx=2, pady=2)

    headerFrame.pack(fill=tk.X)
    browseFrame.pack(fill=tk.BOTH, expand=True)
    footerFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    searchEntry.bind(
        "<Return>",
        partial(search, searchEntry, cwdLabel, items, folderIcon, fileIcon, footer),
    )  # on enter press, run search1
    return cwdLabel, items, folderIcon, fileIcon, footer


def write_theme(theme):
    with open(file_path + "../res/theme.txt", "w") as f:  # closes file automatically
        f.write(theme)
    warning_popup()


def warning_popup():
    Messagebox.show_info(
        message="Please restart the application to apply changes", title="Info"
    )


def drive_stats(window):
    top = tk.Toplevel(window)
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "info.png"))
    top.title("Drives")

    meters = []
    for drive in available_drives:
        shutil.disk_usage(drive)
        meters.append(
            ttk.Meter(
                top,
                bootstyle="default",
                metersize=180,
                padding=5,
                metertype="semi",
                subtext="GB Used",
                textright="/ "
                + str(
                    round(shutil.disk_usage(drive).total / 1 * 10**-9)
                ),  # converts bytes to GB
                textleft=drive,
                interactive=False,
                amounttotal=round(
                    shutil.disk_usage(drive).total / 1 * 10**-9
                ),  # converts bytes to GB
                amountused=round(
                    shutil.disk_usage(drive).used / 1 * 10**-9
                ),  # converts bytes to GB
            )
        )
    top.geometry(str(len(meters) * 200) + "x200")  # Add 200px width for every drive
    for meter in meters:
        meter.pack(side=tk.LEFT, expand=True, fill=tk.X)


def cd_drive(drive, cwdLabel, items, folderIcon, fileIcon, footer, queryNames):
    global fileNames, currDrive
    cwdLabel.config(text=" " + drive)
    currDrive = drive
    fileNames = os.listdir(currDrive)
    os.chdir(currDrive + "/")
    refresh(cwdLabel, items, folderIcon, fileIcon, footer, queryNames)


def up_key(items, event):
    global selectedItem
    iid = items.focus()
    iid = items.prev(iid)
    if iid:
        items.selection_set(iid)
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass


def down_key(items, event):
    global selectedItem
    iid = items.focus()
    iid = items.next(iid)
    if iid:
        items.selection_set(iid)
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass


def click(searchEntry, event):
    if searchEntry.get() == "Search files..":
        searchEntry.delete(0, "end")


def FocusOut(searchEntry, window, event):
    searchEntry.delete(0, "end")
    searchEntry.insert(0, "Search files..")
    window.focus()


def rename_popup(items):
    if items.focus() != "":
        try:
            name = Querybox.get_string(prompt="Name: ", title="Rename")
            old = os.getcwd() + "/" + selectedItem
            os.rename(old, name)
        except:
            pass
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )


def selectItem(items, event):
    global selectedItem
    # selectedItemID = items.focus()
    iid = items.identify_row(event.y)
    if iid:
        items.selection_set(iid)
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass


def about_popup():  # popup window
    Messagebox.ok(
        message="My File Explorer\nMade by: Chris Tsouchlakis\nVersion 0.2.2",
        title="About",
    )


def new_file_popup():
    name: str = Querybox.get_string(prompt="Name: ", title="New file")
    if name != "":
        try:
            f = open(os.getcwd() + "/" + name, "x")
            f.close()
        except:
            pass


def del_file_popup(items):
    if items.focus() != "":  # if there is a focused item
        answer = Messagebox.yesno(
            message="Are you sure?\nThis file/directory will be deleted permanently.",
            alert=True,
        )
        if answer == "Yes":
            del_file()
        else:
            return
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )


def del_file():
    if os.path.isfile(os.getcwd() + "/" + selectedItem):
        os.remove(os.getcwd() + "/" + selectedItem)
    elif os.path.isdir(os.getcwd() + "/" + selectedItem):
        # os.rmdir(os.getcwd() + "/" + selectedItem)
        shutil.rmtree(os.getcwd() + "/" + selectedItem)


def main():
    global theme, file_path
    file_path = os.path.join(os.path.dirname(__file__), "../icons/")
    with open(file_path + "../res/theme.txt") as f:  # closes file automatically
        theme = f.readline()
    if theme == "":  # if theme.txt is empty, set default theme
        theme = Darkly
    # Main window
    root = createWindow()

    cwdLabel, items, folderIcon, fileIcon, footer = create_widgets(root)
    refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])
    root.mainloop()


if __name__ == "__main__":
    main()
