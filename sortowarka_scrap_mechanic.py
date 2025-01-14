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


def Walkthrough():
    for subdir, dirs, files in os.walk(rootdir):
        mt = get_latest_mod_time(subdir)
        readable_time = time.ctime(mt[1])
        print(f"{mt[0]} - last modification time: {readable_time}")
        timestamps[subdir] = mt[1]

    for k, v in timestamps.items():
        # print(f"{k}: {v}")
        os.utime(k, (v, v))


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


count_blueprints()
Walkthrough()
