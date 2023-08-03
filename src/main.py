import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from functools import partial

import ext

# TODO:
# Menu bar preferences,
# grab file icons from files,
# improve extension handling (remove ext.py),
# improve right click functionality,
# editable path,
# column sorting,
# control treeview with arrow keys, open file with enter as well,
# code improvements

# globals
lastDirectory = ""
selectedItem = ""


def createWindow(file_path):
    root = tk.Tk()
    root.title("My File Explorer")
    root.geometry("1024x600")
    root.resizable(True, True)
    root.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))
    return root


def refresh(cwdLabel, items, folderIcon, fileIcon, footer, queryNames):
    # Refresh Header
    cwdLabel.config(text=os.getcwd())
    # --Refresh Header

    # Refresh Browse
    if queryNames:  # if user gave query and pressed enter
        fileNames = queryNames
    else:
        fileNames = os.listdir()
    fileTypes = [None] * len(fileNames)
    fileSizes = [None] * len(fileNames)
    fileDateModified = []
    for i in items.get_children():  # delete data from previous directory
        items.delete(i)
    for i in range(len(fileNames)):
        # modification time of file
        fileDateModified.append(
            datetime.fromtimestamp(os.path.getmtime(fileNames[i])).strftime(
                "%d-%m-%Y %I:%M"
            )
        )
        # size of file
        fileSizes[i] = (
            str(round(os.stat(fileNames[i]).st_size / 1024)) + " KB"
        )  # str->round->size of file in KB
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
                values=(fileNames[i], fileDateModified[i], fileTypes[i], fileSizes[i]),
                image=fileIcon,
            )
    # --Refresh Browse

    # Draw browse
    items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # --Draw browse

    # Refresh Footer
    footer.config(text=str(len(fileNames)) + " files - directories")
    footer.pack()
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
    for item in items.selection():
        tempDictionary = items.item(item)
        tempName = tempDictionary["values"][0]  # get first value of dictionary
    split = os.path.splitext(tempName)  # split file extension
    ext = split[1]
    try:
        newPath = os.getcwd() + "\\" + tempName
        if os.path.isdir(
            newPath
        ):  # if file is directory, open directory else open file
            os.chdir(newPath)
        else:
            os.startfile(newPath)
        refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])
    except:
        os.chdir("../")


def onRightClick(m, event):
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


def draw(file_path, window, s):
    sep = ttk.Separator(window, orient="horizontal")
    sep.pack(fill="x")

    # Browse Frame
    browseFrame = ttk.Frame(window)
    scroll = ttk.Scrollbar(browseFrame)
    items = ttk.Treeview(
        browseFrame,
        columns=("Name", "Date modified", "Type", "Size"),
        yscrollcommand=scroll.set,
        height=15,
    )
    scroll.config(command=items.yview)  # scroll with mouse drag
    # --Browse Frame

    # Footer Frame
    footerFrame = ttk.Frame(window)
    footer = ttk.Label(footerFrame)
    # --Footer Frame

    folderIcon = tk.PhotoImage(file=file_path + "Folder-icon.png", width=20, height=15)
    fileIcon = tk.PhotoImage(file=file_path + "File-icon.png", width=20, height=15)

    # Header Frame
    refreshIcon = tk.PhotoImage(file=file_path + "Very-Basic-Reload-icon.png")
    backArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Back-icon.png")
    frontArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Front-icon.png")
    headerFrame = ttk.Frame()
    cwdLabel = ttk.Label(headerFrame, text=os.getcwd(), relief="groove", width=120)
    searchEntry = ttk.Entry(headerFrame, width=27)
    backButton = ttk.Button(
        headerFrame,
        image=backArrowIcon,
        command=partial(previous, cwdLabel, items, folderIcon, fileIcon, footer),
    )
    forwardButton = ttk.Button(
        headerFrame,
        image=frontArrowIcon,
        command=partial(next, cwdLabel, items, folderIcon, fileIcon, footer),
    )
    refreshButton = ttk.Button(
        headerFrame,
        command=partial(refresh, cwdLabel, items, folderIcon, fileIcon, footer, []),
        image=refreshIcon,
    )
    # keep references
    backButton.img_reference = backArrowIcon
    forwardButton.img_reference = frontArrowIcon
    refreshButton.img_reference = refreshIcon
    # --Header Frame

    # Right click menu
    m = tk.Menu(window, tearoff=False)
    # m.add_command(label="Cut")
    # m.add_command(label="Copy")
    # m.add_command(label="Paste")
    m.add_command(label="New file", command=partial(new_file_popup, window, file_path))
    m.add_command(
        label="Rename selected",
        command=partial(rename_popup, window, file_path, items),
    )
    m.add_command(
        label="Delete selected",
        command=partial(del_file_popup, items, window, file_path),
    )
    m.add_separator()
    m.add_command(
        label="Refresh",
        command=partial(refresh, cwdLabel, items, folderIcon, fileIcon, footer, []),
    )
    # --Right click menu

    s.configure("Treeview", rowheight=30)  # increase row height of Treeview
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
    items.bind("<Button-3>", partial(onRightClick, m))  # command on right click
    # --Browse Frame

    # Menu bar
    bar = tk.Menu(window)
    window.config(menu=bar)

    file_menu = tk.Menu(bar, tearoff=False)
    file_menu.add_command(
        label="New file", command=partial(new_file_popup, window, file_path)
    )
    file_menu.add_command(
        label="Rename selected", command=partial(rename_popup, window, file_path, items)
    )
    file_menu.add_command(
        label="Delete selected",
        command=partial(del_file_popup, items, window, file_path),
    )
    # file_menu.add_command(label="Create directory", command=new_dir)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.destroy)

    about_menu = tk.Menu(bar, tearoff=False)
    about_menu.add_command(
        label="About the app", command=partial(about_popup, window, file_path)
    )

    bar.add_cascade(label="File", menu=file_menu, underline=0)
    bar.add_cascade(label="About", menu=about_menu, underline=0)
    # --Menu bar

    # packs
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    backButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    forwardButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    cwdLabel.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH, expand=True)
    refreshButton.pack(side=tk.LEFT, padx=1, pady=10, fill=tk.BOTH)
    searchEntry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)

    headerFrame.pack(fill=tk.X)
    browseFrame.pack(fill=tk.BOTH, expand=True)
    footerFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    searchEntry.bind(
        "<Return>",
        partial(search, searchEntry, cwdLabel, items, folderIcon, fileIcon, footer),
    )  # on enter press, run search1
    return cwdLabel, items, folderIcon, fileIcon, footer


def rename_popup(window, file_path, items):
    top = tk.Toplevel(window)
    top.geometry("200x50")
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))
    if items.focus() != "":
        top.title("Rename selected")

        lb = ttk.Label(top, text="New name:")
        nameEntry = ttk.Entry(top, width=25)

        lb.pack()
        nameEntry.pack()

        nameEntry.bind("<Return>", partial(rename_f, nameEntry, top))
    else:
        top.title("Info")
        lb = ttk.Label(top, text="There is no selected file or directory.")
        lb.pack()


def rename_f(nameEntry, top, event):
    old = os.getcwd() + "\\" + selectedItem
    os.rename(old, nameEntry.get())
    top.destroy()


def selectItem(items, event):
    global selectedItem
    selectedItemID = items.focus()
    selectedItem = items.item(selectedItemID)["values"][0]


def about_popup(window, file_path):  # popup window
    top = tk.Toplevel(window)
    top.geometry("300x100")
    top.title("About")
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))

    lb = ttk.Label(top, text="My file explorer")
    lb2 = ttk.Label(top, text="Made by: Chris Tsouchlakis")
    lb3 = ttk.Label(top, text="Version 0.1.0")

    lb.pack(pady=10)
    lb2.pack(pady=1)
    lb3.pack(pady=1)


def new_file_popup(window, file_path):
    top = tk.Toplevel(window)
    top.geometry("200x50")
    top.title("New file")
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))

    lb = ttk.Label(top, text="File name:")
    nameEntry = ttk.Entry(top, width=25)

    lb.pack()
    nameEntry.pack()

    nameEntry.bind("<Return>", partial(new_file, nameEntry, top))


def new_file(nameEntry, top, event):
    if nameEntry.get() != "":
        open(os.getcwd() + "\\" + nameEntry.get(), "x")
        top.destroy()


def del_file_popup(items, window, file_path):
    top = tk.Toplevel(window)
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))

    if items.focus() != "":  # if there is a focused item
        top.title("Warning")
        top.geometry("200x100")

        lb = ttk.Label(
            top, text="Are you sure?\nThis file/directory will be deleted permanently."
        )
        delbtn = ttk.Button(
            top,
            text="DELETE",
            command=partial(del_file, top),
        )
        cnbtn = ttk.Button(top, text="CANCEL", command=top.destroy)

        lb.pack()
        delbtn.pack(padx=5)
        cnbtn.pack()
    else:
        top.geometry("200x50")
        top.title("Info")
        lb = ttk.Label(top, text="There is no selected file or directory.")
        lb.pack()


def del_file(top):
    if os.path.isfile(os.getcwd() + "\\" + selectedItem):
        os.remove(os.getcwd() + "\\" + selectedItem)
    elif os.path.isdir(os.getcwd() + "\\" + selectedItem):
        os.rmdir(os.getcwd() + "\\" + selectedItem)
    top.destroy()


def main():
    file_path = os.path.join(os.path.dirname(__file__), "..\\icons\\")
    # Main window
    root = createWindow(file_path)
    s = ttk.Style()

    cwdLabel, items, folderIcon, fileIcon, footer = draw(file_path, root, s)
    refresh(cwdLabel, items, folderIcon, fileIcon, footer, [])
    root.mainloop()


if __name__ == "__main__":
    main()
