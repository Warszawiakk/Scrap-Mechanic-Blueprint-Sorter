import json
import os
import time
from time import sleep
from datetime import datetime
import pathlib
import shutil

from tkinter import *
from tkinter import ttk

# UI ================================================================================================================================ \/

window = Tk()
window.title("Scrap Mechanic Blueprint Sorter")
window.geometry("900x250")
window.tk.call("tk", "scaling", 2.0)

entry_string = ""
rootdir = ""


def display_text():
    global entry
    global entry_string
    entry_string = entry.get()
    labelka.configure(text=entry_string)
    print(f"Wprowadzono: {entry_string}")


labelka = Label(window, text="", font=("Courier 5 bold"))
labelka.pack()

tekst = Label(window, text="please enter full path to Blueprints folder: ")
tekst.pack()

entry = Entry(window, width=40)
entry.focus_set()
entry.pack()


def executeOrder66():
    display_text()

    raw_rootdir = entry_string
    unchanged_rootdir = pathlib.PureWindowsPath(raw_rootdir)
    print(unchanged_rootdir)
    global rootdir
    rootdir = str(unchanged_rootdir.as_posix())
    print(rootdir)

    Sort_Blueprints()
    Rename_Folders()
    count_blueprints()

    end_tekst = Label(window, text="Done!")
    end_tekst.pack()


ttk.Button(window, text="Okay", width=20, command=executeOrder66).pack(pady=20)


# UI ================================================================================================================================ /\

timestamps: dict[str, float] = {}

end_of_sequence = False


def count_blueprints():
    loops = 0
    for subdir in os.walk(rootdir):
        loops = loops + 1
    print(
        f"""
    Total blueprints: {round((loops-1)/2)}
    """
    )
    blueprint_count = Label(window, text=f"Total blueprints: {round((loops - 1) / 2)}")
    blueprint_count.pack()


def Sort_Blueprints():
    print("Root: ", rootdir)
    for subdir, dirs, files in os.walk(rootdir):
        if subdir == rootdir:
            continue
        mt = get_latest_mod_time(subdir)
        timestamps[subdir] = mt[1]
        readable_time = time.ctime(mt[1])
        print(f"{mt[0]} - last modification time: {readable_time}")

    for k, v in timestamps.items():
        os.utime(k, (v, v))
    print("Blueprints sorted")


def Rename_Folders():
    nonamecount = 0
    for subdir, dirs, files in os.walk(rootdir):
        if subdir == rootdir:
            continue
        try:
            subdir = subdir.replace("\\", "/")
            with open(subdir + "/description.json", encoding="utf-8") as open_json:
                data = json.load(open_json)

            if data["name"] == "":
                nonamecount += 1
                data["name"] = "BezNazwy_" + str(nonamecount)
            newName = (
                subdir.rsplit("/", 1)[0]
                + "/"
                + data["name"]
                .replace("\\", "/")
                .replace("/", "_")
                .replace('"', "_")
                .replace("?", "__znak_zapytania__")
                .replace(".", "_dot_")
                .replace("<", "__less_than__")
                .replace(">", "__greater_than__")
                .replace(":", "-")
                .replace("|", "l")
                .replace("*", "x")
            )

            os.rename(subdir, newName)
            print("Folder renamed at: " + subdir)
        except Exception as e:
            print("\n\nFolder rename failed at: ", subdir, "\nexception:", e)
    print("Folders renamed.")


def get_latest_mod_time(rootdir) -> tuple[str, int]:
    latest_time = 0
    result_path = ""
    for root, _, files in os.walk(rootdir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mod_time = os.path.getmtime(file_path)
                if latest_time < mod_time:
                    result_path = file_path
                    latest_time = mod_time
            except FileNotFoundError:
                pass
    return (result_path, latest_time)


window.mainloop()
