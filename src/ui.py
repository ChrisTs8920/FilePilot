import ttkbootstrap as ttk
import tkinter as tk
from datetime import datetime
import globals
import psutil
import func
import ext
import os

from functools import partial
from PIL import Image, ImageTk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.dialogs.dialogs import Querybox
from ttkbootstrap.tooltip import ToolTip


def create_window():
    # root = tk.Tk()
    root = ttk.Window(themename=globals.theme)
    root.title("FilePilot")
    root.geometry("1280x720")
    root.resizable(True, True)
    root.iconphoto(False, tk.PhotoImage(file=globals.file_path + "light/app.png"))
    return root


def refresh(queryNames):
    # Refresh Header
    globals.cwdLabel.config(text=" " + os.getcwd().replace('\\', "  >  "), font=("TkDefaultFont", globals.font_size, "bold"))
    # --Refresh Header

    # Refresh Browse
    fileSizesSum = 0
    if queryNames:  # if user gave query and pressed enter
        globals.fileNames = queryNames
    else:
        globals.fileNames = os.listdir(os.getcwd())
    fileTypes = [""] * len(globals.fileNames)
    fileSizes = [""] * len(globals.fileNames)
    fileDateModified = []
    for i in globals.items.get_children():  # delete data from previous directory
        globals.items.delete(i)
    for i in range(len(globals.fileNames)):
        try:
            # modification time of file
            fileDateModified.append(
                datetime.fromtimestamp(os.path.getmtime(globals.fileNames[i])).strftime(
                    "%d-%m-%Y %I:%M"
                )
            )
            # size of file
            fileSizes[i] = str(
                round(os.stat(globals.fileNames[i]).st_size / 1024)
            )  # str->round->size of file in KB
            fileSizesSum += int(fileSizes[i])
            fileSizes[i] = str(round(os.stat(globals.fileNames[i]).st_size / 1024)) + " KB"
            # check file type
            ext.extensions(fileTypes, globals.fileNames, i)

            # insert
            if fileTypes[i] == "Directory":
                globals.items.insert(
                    parent="",
                    index=i,
                    values=(globals.fileNames[i], fileDateModified[i], fileTypes[i], ""),
                    image=globals.folderIcon[0],
                )
            else:
                globals.items.insert(
                    parent="",
                    index=i,
                    values=(
                        globals.fileNames[i],
                        fileDateModified[i],
                        fileTypes[i],
                        fileSizes[i],
                    ),
                    image=globals.fileIcon[0],
                )
        except Exception as e:
            print(e)
            pass
    # --Refresh Browse

    # Draw browse
    globals.items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # --Draw browse

    # Refresh Footer
    globals.footer.config(
        text=" "
        + str(len(globals.fileNames))
        + " items | "
        + str(round(fileSizesSum / 1024, 1))
        + " MB Total"
    )
    globals.footer.pack(fill=tk.BOTH)
    # --Refresh Footer


def create_widgets(window):
    s = ttk.Style()

    # Color selection for theme
    if (globals.theme_mode == "dark"):
        bootstyle = "dark"
    else:
        bootstyle = "light"

    # Browse Frame
    browseFrame = ttk.Frame(window)
    scroll = ttk.Scrollbar(browseFrame, orient="vertical")
    globals.items = ttk.Treeview(
        browseFrame,
        columns=("Name", "Date modified", "Type", "Size"),
        yscrollcommand=scroll.set,
        height=15,
        style="Custom.Treeview",
    )
    scroll.config(command=globals.items.yview)  # scroll with mouse drag
    # --Browse Frame

    # Footer Frame
    footerFrame = ttk.Frame(window)
    globals.footer = ttk.Label(footerFrame)
    grip = ttk.Sizegrip(footerFrame, bootstyle=bootstyle)
    # --Footer Frame

    # Setup icons
    if (globals.theme_mode == "light"):
        globals.folderIcon = [tk.PhotoImage(file=globals.file_path + "light/Folder-icon.png"), "light/Folder-icon.png"]
        globals.fileIcon = [tk.PhotoImage(file=globals.file_path + "light/File-icon.png"), "light/File-icon.png"]
        globals.backIcon = [tk.PhotoImage(file=globals.file_path + "light/back.png"), "light/back.png"]
        globals.frontIcon = [tk.PhotoImage(file=globals.file_path + "light/front.png"), "light/front.png"]
        globals.copyIcon = [tk.PhotoImage(file=globals.file_path + "light/copy.png"), "light/copy.png"]
        globals.cpuIcon = [tk.PhotoImage(file=globals.file_path + "light/cpu.png"), "light/cpu.png"]
        globals.deleteIcon = [tk.PhotoImage(file=globals.file_path + "light/delete.png"), "light/delete.png"]
        globals.driveIcon = [tk.PhotoImage(file=globals.file_path + "light/drive.png"), "light/drive.png"]
        globals.fontIcon = [tk.PhotoImage(file=globals.file_path + "light/font.png"), "light/font.png"]
        globals.appIcon = [tk.PhotoImage(file=globals.file_path + "light/app.png"), "light/app.png"]
        globals.infoIcon = [tk.PhotoImage(file=globals.file_path + "light/info.png"), "light/info.png"]
        globals.memoryIcon = [tk.PhotoImage(file=globals.file_path + "light/memory.png"), "light/memory.png"]
        globals.networkIcon = [tk.PhotoImage(file=globals.file_path + "light/network.png"), "light/network.png"]
        globals.pasteIcon = [tk.PhotoImage(file=globals.file_path + "light/paste.png"), "light/paste.png"]
        globals.pieIcon = [tk.PhotoImage(file=globals.file_path + "light/pie.png"), "light/pie.png"]
        globals.processIcon = [tk.PhotoImage(file=globals.file_path + "light/process.png"), "light/process.png"]
        globals.reloadIcon = [tk.PhotoImage(file=globals.file_path + "light/reload.png"), "light/reload.png"]
        globals.renameIcon = [tk.PhotoImage(file=globals.file_path + "light/rename.png"), "light/rename.png"]
        globals.scaleIcon = [tk.PhotoImage(file=globals.file_path + "light/scale.png"), "light/scale.png"]
        globals.themesIcon = [tk.PhotoImage(file=globals.file_path + "light/themes.png"), "light/themes.png"]
        globals.exitIcon = [tk.PhotoImage(file=globals.file_path + "light/exit.png"), "light/exit.png"]
    else:
        globals.folderIcon = [tk.PhotoImage(file=globals.file_path + "dark/Folder-icon.png"), "dark/Folder-icon.png"]
        globals.fileIcon = [tk.PhotoImage(file=globals.file_path + "dark/File-icon.png"), "dark/File-icon.png"]
        globals.backIcon = [tk.PhotoImage(file=globals.file_path + "dark/back.png"), "dark/back.png"]
        globals.frontIcon = [tk.PhotoImage(file=globals.file_path + "dark/front.png"), "dark/front.png"]
        globals.copyIcon = [tk.PhotoImage(file=globals.file_path + "dark/copy.png"), "dark/copy.png"]
        globals.cpuIcon = [tk.PhotoImage(file=globals.file_path + "dark/cpu.png"), "dark/cpu.png"]
        globals.deleteIcon = [tk.PhotoImage(file=globals.file_path + "dark/delete.png"), "dark/delete.png"]
        globals.driveIcon = [tk.PhotoImage(file=globals.file_path + "dark/drive.png"), "dark/drive.png"]
        globals.fontIcon = [tk.PhotoImage(file=globals.file_path + "dark/font.png"), "dark/font.png"]
        globals.appIcon = [tk.PhotoImage(file=globals.file_path + "dark/app.png"), "dark/app.png"]
        globals.infoIcon = [tk.PhotoImage(file=globals.file_path + "dark/info.png"), "dark/info.png"]
        globals.memoryIcon = [tk.PhotoImage(file=globals.file_path + "dark/memory.png"), "dark/memory.png"]
        globals.networkIcon = [tk.PhotoImage(file=globals.file_path + "dark/network.png"), "dark/network.png"]
        globals.pasteIcon = [tk.PhotoImage(file=globals.file_path + "dark/paste.png"), "dark/paste.png"]
        globals.pieIcon = [tk.PhotoImage(file=globals.file_path + "dark/pie.png"), "dark/pie.png"]
        globals.processIcon = [tk.PhotoImage(file=globals.file_path + "dark/process.png"), "dark/process.png"]
        globals.reloadIcon = [tk.PhotoImage(file=globals.file_path + "dark/reload.png"), "dark/reload.png"]
        globals.renameIcon = [tk.PhotoImage(file=globals.file_path + "dark/rename.png"), "dark/rename.png"]
        globals.scaleIcon = [tk.PhotoImage(file=globals.file_path + "dark/scale.png"), "dark/scale.png"]
        globals.themesIcon = [tk.PhotoImage(file=globals.file_path + "dark/themes.png"), "dark/themes.png"]
        globals.exitIcon = [tk.PhotoImage(file=globals.file_path + "dark/exit.png"), "dark/exit.png"]

    # Header Frame
    refreshIcon = tk.PhotoImage(file=globals.file_path + globals.reloadIcon[1])
    backArrowIcon = tk.PhotoImage(file=globals.file_path + globals.backIcon[1])
    frontArrowIcon = tk.PhotoImage(file=globals.file_path + globals.frontIcon[1])
    headerFrame = ttk.Frame()
    globals.cwdLabel = ttk.Label(
        headerFrame,
        text=" " + os.getcwd(),
        relief="flat",
        # width=110,
    )
    searchEntry = ttk.Entry(headerFrame, width=30, font=("TkDefaultFont", globals.font_size))
    searchEntry.insert(0, "Search files..")
    searchEntry.bind("<Button-1>", partial(func.click, searchEntry))
    searchEntry.bind("<FocusOut>", partial(func.focus_out, searchEntry, window))
    backButton = ttk.Button(
        headerFrame,
        image=backArrowIcon,
        command=func.previous,
        bootstyle=bootstyle,
    )
    forwardButton = ttk.Button(
        headerFrame,
        image=frontArrowIcon,
        command=func.next,
        bootstyle=bootstyle,
    )
    refreshButton = ttk.Button(
        headerFrame,
        command=partial(refresh, []),
        image=refreshIcon,
        bootstyle=bootstyle,
    )

    # tooltips for buttons
    ToolTip(backButton, text="Back", bootstyle=("default", "inverse"))
    ToolTip(forwardButton, text="Forward", bootstyle=("default", "inverse"))
    ToolTip(refreshButton, text="Refresh", bootstyle=("default", "inverse"))
    # --Header Frame

    # imgs
    open_img = Image.open(globals.file_path + globals.appIcon[1])
    open_photo = ImageTk.PhotoImage(open_img)

    refresh_img = Image.open(globals.file_path + globals.reloadIcon[1])
    refresh_photo = ImageTk.PhotoImage(refresh_img)

    rename_img = Image.open(globals.file_path + globals.renameIcon[1])
    rename_photo = ImageTk.PhotoImage(rename_img)

    drive_img = Image.open(globals.file_path + globals.driveIcon[1])
    drive_photo = ImageTk.PhotoImage(drive_img)

    info_img = Image.open(globals.file_path + globals.infoIcon[1])
    info_photo = ImageTk.PhotoImage(info_img)

    pie_img = Image.open(globals.file_path + globals.pieIcon[1])
    pie_photo = ImageTk.PhotoImage(pie_img)

    cpu_img = Image.open(globals.file_path + globals.cpuIcon[1])
    cpu_photo = ImageTk.PhotoImage(cpu_img)

    memory_img = Image.open(globals.file_path + globals.memoryIcon[1])
    memory_photo = ImageTk.PhotoImage(memory_img)

    network_img = Image.open(globals.file_path + globals.networkIcon[1])
    network_photo = ImageTk.PhotoImage(network_img)

    process_img = Image.open(globals.file_path + globals.processIcon[1])
    process_photo = ImageTk.PhotoImage(process_img)

    file_img = Image.open(globals.file_path + globals.fileIcon[1])
    file_photo = ImageTk.PhotoImage(file_img)

    dir_img = Image.open(globals.file_path + globals.folderIcon[1])
    dir_photo = ImageTk.PhotoImage(dir_img)

    themes_img = Image.open(globals.file_path + globals.themesIcon[1])
    themes_photo = ImageTk.PhotoImage(themes_img)

    scale_img = Image.open(globals.file_path + globals.scaleIcon[1])
    scale_photo = ImageTk.PhotoImage(scale_img)

    font_img = Image.open(globals.file_path + globals.fontIcon[1])
    font_photo = ImageTk.PhotoImage(font_img)

    copy_img = Image.open(globals.file_path + globals.copyIcon[1])
    copy_photo = ImageTk.PhotoImage(copy_img)

    paste_img = Image.open(globals.file_path + globals.pasteIcon[1])
    paste_photo = ImageTk.PhotoImage(paste_img)

    delete_img = Image.open(globals.file_path + globals.deleteIcon[1])
    delete_photo = ImageTk.PhotoImage(delete_img)

    # Right click menu
    m = ttk.Menu(window, tearoff=False, font=("TkDefaultFont", globals.font_size))
    m.add_command(
        label="Open",
        image=open_photo,
        compound="left",
        command=func.on_double_click,
    )
    m.add_separator()
    m.add_command(
        label="New file", image=file_photo, compound="left", command=new_file_popup
    )
    m.add_command(
        label="New directory", image=dir_photo, compound="left", command=new_dir_popup
    )
    m.add_separator()
    m.add_command(
        label="Copy",
        image=copy_photo,
        compound="left",
        command=func.copy,
    )
    m.add_command(
        label="Paste", image=paste_photo, compound="left", command=func.paste
    )
    m.add_command(
        label="Delete",
        image=delete_photo,
        compound="left",
        command=del_file_popup,
    )
    m.add_command(
        label="Rename",
        image=rename_photo,
        compound="left",
        command=rename_popup,
    )
    m.add_separator()
    m.add_command(
        label="Refresh",
        image=refresh_photo,
        compound="left",
        command=partial(refresh, []),
    )
    # --Right click menu

    s.configure(".", font=("TkDefaultFont", globals.font_size))  # set font size
    s.configure("Treeview", rowheight=28)  # customize treeview
    s.configure(
        "Treeview.Heading", font=("TkDefaultFont", str(int(globals.font_size) + 1), "bold")
    )
    s.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # remove borders

    globals.items.column("#0", width=40, stretch=tk.NO)
    globals.items.column("Name", anchor=tk.W, width=150, minwidth=120)
    globals.items.column("Date modified", anchor=tk.CENTER, width=200, minwidth=120)
    globals.items.column("Size", anchor=tk.CENTER, width=80, minwidth=60)
    globals.items.column("Type", anchor=tk.CENTER, width=120, minwidth=60)
    globals.items.heading(
        "Name",
        text="Name",
        anchor=tk.CENTER,
        command=partial(func.sort_col, "Name", False),
    )
    globals.items.heading(
        "Date modified",
        text="Date modified",
        anchor=tk.CENTER,
        command=partial(func.sort_col, "Date modified", False),
    )
    globals.items.heading(
        "Type",
        text="Type",
        anchor=tk.CENTER,
        command=partial(func.sort_col, "Type", False),
    )
    globals.items.heading(
        "Size",
        text="Size",
        anchor=tk.CENTER,
        command=partial(func.sort_col, "Size", False),
    )
    globals.items.bind(
        "<Double-1>",
        func.on_double_click,
    )  # command on double click
    globals.items.bind("<ButtonRelease-1>", func.select_item)
    globals.items.bind("<Button-3>", partial(func.on_right_click, m))  # command on right click
    globals.items.bind("<Up>", func.up_key)  # bind up arrow key
    globals.items.bind("<Down>", func.down_key)  # bind down arrow key
    # --Browse Frame

    # Menu bar
    bar = ttk.Menu(window, font=("TkDefaultFont", globals.font_size))
    window.config(menu=bar)

    file_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    file_menu.add_command(
        label="Open",
        image=open_photo,
        compound="left",
        command=func.on_double_click,
    )
    file_menu.add_command(
        label="New file",
        image=file_photo,
        compound="left",
        command=new_file_popup,
    )
    file_menu.add_command(
        label="New directory", image=dir_photo, compound="left", command=new_dir_popup
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Copy Selected",
        image=copy_photo,
        compound="left",
        command=func.copy,
    )
    file_menu.add_command(
        label="Paste Selected", image=paste_photo, compound="left", command=func.paste
    )
    file_menu.add_command(
        label="Delete selected",
        image=delete_photo,
        compound="left",
        command=del_file_popup,
    )
    file_menu.add_command(
        label="Rename selected",
        image=rename_photo,
        compound="left",
        command=rename_popup,
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Exit", 
        image=globals.exitIcon[0],
        compound="left",
        command=window.destroy)

    drives_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    for drive in globals.available_drives:
        drives_menu.add_command(
            label=drive,
            image=drive_photo,
            compound="left",
            command=partial(func.cd_drive, drive, []),
        )

    system_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    system_menu.add_command(
        label="Drives",
        image=pie_photo,
        compound="left",
        command=partial(drive_stats, window),
    )
    system_menu.add_command(
        label="CPU", image=cpu_photo, compound="left", command=cpu_stats
    )
    system_menu.add_command(
        label="Memory", image=memory_photo, compound="left", command=memory_stats
    )
    system_menu.add_command(
        label="Network", image=network_photo, compound="left", command=network_stats
    )
    system_menu.add_command(
        label="Processes",
        image=process_photo,
        compound="left",
        command=partial(processes_win, window),
    )

    sub_themes = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    sub_themes.add_command(label="Darkly", command=partial(func.write_theme, globals.Darkly))
    sub_themes.add_command(label="Solar Dark", command=partial(func.write_theme, globals.solarD))
    sub_themes.add_command(
        label="Superhero Dark", command=partial(func.write_theme, globals.superheroD)
    )
    sub_themes.add_command(label="Cyborg Dark", command=partial(func.write_theme, globals.CyborgD))
    sub_themes.add_command(label="Vapor Dark", command=partial(func.write_theme, globals.VaporD))
    sub_themes.add_separator()
    sub_themes.add_command(label="Litera Light", command=partial(func.write_theme, globals.literaL))
    sub_themes.add_command(label="Minty Light", command=partial(func.write_theme, globals.mintyL))
    sub_themes.add_command(label="Morph Light", command=partial(func.write_theme, globals.morphL))
    sub_themes.add_command(label="Yeti Light", command=partial(func.write_theme, globals.yetiL))

    sub_font_size = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    sub_font_size.add_command(label="14", command=partial(change_font_popup, 14))
    sub_font_size.add_command(label="12", command=partial(change_font_popup, 12))
    sub_font_size.add_command(label="11", command=partial(change_font_popup, 11))
    sub_font_size.add_command(
        label="10 - default", command=partial(change_font_popup, 10)
    )
    sub_font_size.add_command(label="9", command=partial(change_font_popup, 9))
    sub_font_size.add_command(label="8", command=partial(change_font_popup, 8))
    sub_font_size.add_command(label="7", command=partial(change_font_popup, 7))

    sub_scale = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    sub_scale.add_command(label="150%", command=partial(func.change_scale, 1.5, s))
    sub_scale.add_command(label="125%", command=partial(func.change_scale, 1.25, s))
    sub_scale.add_command(label="100%", command=partial(func.change_scale, 1.0, s))
    sub_scale.add_command(label="75%", command=partial(func.change_scale, 0.75, s))
    sub_scale.add_command(label="50%", command=partial(func.change_scale, 0.5, s))

    preferences_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    preferences_menu.add_cascade(
        label="Themes", image=themes_photo, compound="left", menu=sub_themes
    )
    preferences_menu.add_cascade(
        label="Scale", image=scale_photo, compound="left", menu=sub_scale
    )
    preferences_menu.add_cascade(
        label="Font size", image=font_photo, compound="left", menu=sub_font_size
    )

    help_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    help_menu.add_command(
        label="Keybinds", image=info_photo, compound="left", command=keybinds
    )

    about_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", globals.font_size))
    about_menu.add_command(
        label="About FilePilot", command=about_popup, image=info_photo, compound="left"
    )

    bar.add_cascade(label="File", menu=file_menu, underline=0)
    bar.add_cascade(label="Drives", menu=drives_menu, underline=0)
    bar.add_cascade(label="System", menu=system_menu, underline=0)
    bar.add_cascade(label="Preferences", menu=preferences_menu, underline=0)
    bar.add_cascade(label="Help", menu=help_menu, underline=0)
    bar.add_cascade(label="About", menu=about_menu, underline=0)
    # --Menu bar

    # packs
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    backButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    forwardButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    globals.cwdLabel.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH, expand=True)
    refreshButton.pack(side=tk.LEFT, padx=1, pady=10, fill=tk.BOTH)
    searchEntry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    grip.pack(side=tk.RIGHT, fill=tk.BOTH, padx=2, pady=2)

    headerFrame.pack(fill=tk.X)
    browseFrame.pack(fill=tk.BOTH, expand=True)
    footerFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    searchEntry.bind(
        "<Return>",
        partial(func.search, searchEntry),
    )  # on enter press, run search1

    # img references
    globals.photo_ref.append(backArrowIcon)
    globals.photo_ref.append(frontArrowIcon)
    globals.photo_ref.append(refreshIcon)
    globals.photo_ref.append(open_photo)
    globals.photo_ref.append(refresh_photo)
    globals.photo_ref.append(rename_photo)
    globals.photo_ref.append(drive_photo)
    globals.photo_ref.append(info_photo)
    globals.photo_ref.append(pie_photo)
    globals.photo_ref.append(cpu_photo)
    globals.photo_ref.append(memory_photo)
    globals.photo_ref.append(network_photo)
    globals.photo_ref.append(process_photo)
    globals.photo_ref.append(file_photo)
    globals.photo_ref.append(dir_photo)
    globals.photo_ref.append(themes_photo)
    globals.photo_ref.append(scale_photo)
    globals.photo_ref.append(font_photo)
    globals.photo_ref.append(copy_photo)
    globals.photo_ref.append(paste_photo)
    globals.photo_ref.append(delete_photo)

    # wrappers for keybinds
    window.bind("<F5>", wrap_refresh)
    window.bind("<Delete>", wrap_del)
    window.bind("<Control-c>", wrap_copy)
    window.bind("<Control-v>", wrap_paste)
    window.bind("<Control-Shift-N>", wrap_new_dir)


# func wrappers
def wrap_refresh(event):  # wrapper for F5 bind
    refresh([])


def wrap_new_dir(event):
    new_dir_popup()


def wrap_copy(event):  # wrapper for ctrl+c keybinds
    func.copy()


def wrap_paste(event):  # wrapper for ctrl+v keybinds
    func.paste()


def wrap_del(event):  # wrapper for delete keybind
    del_file_popup()


# popups
def warning_popup():
    Messagebox.show_info(
        message="Please restart the application to apply changes.", title="Info"
    )


def change_font_popup(size):
    warning_popup()
    func.change_font_size(size)


def keybinds():
    Messagebox.ok(
        message="Copy - <Control + C>\nPaste - <Control + V>\nDelete - <Del>\n"
        + "New Directory - <Control + Shift + N>\nRefresh - <F5>\n"
        + "Select up - <Arrow key up>\nSelect down - <Arrow key down>",
        title="Info",
    )


def about_popup():  # popup window
    Messagebox.ok(
        message="FilePilot\nMade by: Chris Tsouchlakis\nVersion 0.6.0\nMIT License",
        title="About",
    )


def new_file_popup():
    name = Querybox.get_string(prompt="Name: ", title="New file")
    if name is None:
        name = ""
    if name != "":
        try:
            f = open(os.getcwd() + "/" + name, "x")
            f.close()
            refresh([])
        except Exception as e:
            print(e)
            pass


def new_dir_popup():
    name = Querybox.get_string(prompt="Name: ", title="New directory")
    if name is None:
        name = ""
    if name != "":
        try:
            os.mkdir(os.getcwd() + "/" + name)
            refresh([])
        except Exception as e:
            print(e)
            pass


def rename_popup():
    if globals.items.focus() != "":
        try:
            name = Querybox.get_string(prompt="Name: ", title="Rename")
            old = os.getcwd() + "/" + globals.selectedItem
            if name is None:
                name = ""
            os.rename(old, name)
            refresh([])
        except Exception as e:
            print(e)
            pass
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )


def paste_popup(t1):
    top = ttk.Toplevel(title="Progress")
    top.geometry("250x50")
    top.resizable(False, False)

    gauge = ttk.Floodgauge(
        top, bootstyle="success", mode="indeterminate", text="Copying files.."
    )
    gauge.pack(fill=tk.BOTH, expand=tk.YES)
    gauge.start()
    t1.join()
    refresh([])
    top.destroy()


def del_file_popup():
    if globals.items.focus() != "":  # if there is a focused item
        answer = Messagebox.yesno(
            message="Are you sure?\nThis file/directory will be deleted permanently.",
            alert=True,
        )
        if answer == "Yes":
            func.del_file()
            refresh([])
        else:
            return
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )


# System menu
def drive_stats(window):
    top = ttk.Toplevel(window)
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=globals.file_path + globals.infoIcon[1]))
    top.title("Drives")

    meters = []
    for drive in globals.available_drives:
        meters.append(
            ttk.Meter(
                top,
                bootstyle="default",
                metersize=180,
                meterthickness=15,
                stripethickness=2,
                padding=5,
                metertype="full",
                subtext="GB Used",
                textright="/ "
                + str(
                    round(psutil.disk_usage(drive).total / (1024 * 1024 * 1024))
                ),  # converts bytes to GB
                textleft=drive,
                interactive=False,
                amounttotal=round(
                    psutil.disk_usage(drive).total / (1024 * 1024 * 1024)
                ),  # converts bytes to GB
                amountused=round(
                    psutil.disk_usage(drive).used / (1024 * 1024 * 1024)
                ),  # converts bytes to GB
            )
        )
    top.geometry(str(len(meters) * 200) + "x200")  # Add 200px width for every drive
    for meter in meters:
        meter.pack(side=tk.LEFT, expand=True, fill=tk.X)


def cpu_stats():
    cpu_count_log = psutil.cpu_count()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_per = psutil.cpu_percent()
    cpu_freq = round(psutil.cpu_freq().current / 1000, 2)
    Messagebox.ok(
        message="Usage: "
        + str(cpu_per)
        + "%"
        + "\nLogical Processors: "
        + str(cpu_count)
        + "\nCores: "
        + str(cpu_count_log)
        + "\nFrequency: "
        + str(cpu_freq)
        + " GHz",
        title="CPU",
    )


def memory_stats():
    memory_per = psutil.virtual_memory().percent
    memory_total = round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)
    memory_used = round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2)
    memory_avail = round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2)
    Messagebox.ok(
        message="Usage: "
        + str(memory_per)
        + "%"
        + "\nTotal: "
        + str(memory_total)
        + " GB"
        + "\nUsed: "
        + str(memory_used)
        + " GB"
        + "\nAvailable: "
        + str(memory_avail)
        + " GB",
        title="Memory",
    )


def network_stats():
    net = psutil.net_io_counters(pernic=True)
    mes = ""
    for key, value in net.items():
        mes += (
            str(key)
            + ":\n"
            + "Sent: "
            + str(round(value.bytes_sent / (1024 * 1024 * 1024), 2))
            + " GB\n"
            + "Received: "
            + str(round(value.bytes_recv / (1024 * 1024 * 1024), 2))
            + " GB\n\n"
        )
    Messagebox.ok(message=mes, title="Network")


def processes_win(window):
    top = ttk.Toplevel(window)
    top.geometry("1024x600")
    top.resizable(True, True)
    top.iconphoto(False, tk.PhotoImage(file=globals.file_path + globals.processIcon[1]))
    top.title("Processes")
    scroll = ttk.Scrollbar(top, orient="vertical")

    processes_list = []
    for i in psutil.pids():
        p = psutil.Process(i)
        processes_list.append(
            (p.name(), p.pid, p.status(), str(round(p.memory_info().rss / 1024)) + "KB")
        )

    processes = ttk.Treeview(
        top,
        columns=("Name", "PID", "Status", "Memory"),
        yscrollcommand=scroll.set,
        style="Custom.Treeview",
    )
    for p in processes_list:
        processes.insert(parent="", index=0, values=p)
    processes.heading("Name", text="Name", anchor="w")
    processes.heading("PID", text="PID", anchor="w")
    processes.heading("Status", text="Status", anchor="w")
    processes.heading("Memory", text="Memory", anchor="w")
    scroll.config(command=processes.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    processes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
