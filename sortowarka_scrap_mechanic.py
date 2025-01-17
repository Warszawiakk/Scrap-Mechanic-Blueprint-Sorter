import json
import os
import time
from time import sleep
from datetime import datetime
import pathlib
import shutil


print(
    """
Please enter your full blueprint folder location: 
"""
)

timestamps: dict[str, float] = {}

raw_rootdir = input(">>> ")
unchanged_rootdir = pathlib.PureWindowsPath(raw_rootdir)
print(unchanged_rootdir)
rootdir = str(unchanged_rootdir.as_posix())
print(rootdir)


def count_blueprints():
    loops = 0
    for subdir in os.walk(rootdir):
        loops = loops + 1
    print(
        f"""
    Total blueprints: {loops-1}
    """
    )


def Sort_Blueprints():
    print("Root: ", rootdir)
    for subdir, dirs, files in os.walk(rootdir):
        if subdir == rootdir:
            continue
        mt = get_latest_mod_time(subdir)
        timestamps[subdir] = mt[1]
        print("Sub: ", subdir)

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
        except Exception as e:
            print("\n\nFolder rename failed at: ", subdir, "\nexception:", e)
    print("Folders renamed. Done.")


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


Sort_Blueprints()
Rename_Folders()
count_blueprints()

# readable_time = time.ctime(mt[1])
# print(f"{mt[0]} - last modification time: {readable_time}")
