import os
import time
from datetime import datetime
import pathlib


print("""

Please enter your full blueprint folder location: 
""")
raw_rootdir = input(">>> ")
unchanged_rootdir = pathlib.PureWindowsPath(raw_rootdir)
print(unchanged_rootdir)
rootdir = str(unchanged_rootdir.as_posix())
print(rootdir)

def count_blueprints():
    loops = 0
    for subdir in os.walk(rootdir):
        loops = loops+1
    print(f"""
    Total blueprints: {loops-1}
    """)


def get_latest_mod_time(rootdir):
    latest_time = 0
    for root, _, files in os.walk(rootdir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mod_time = os.path.getmtime(file_path)
                latest_time = max(latest_time, mod_time)
            except FileNotFoundError:
                pass
    return latest_time

def print_sorted():
    folders = [os.path.join(rootdir, folder) for folder in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, folder))]
    sorted_folders = sorted(folders, key=get_latest_mod_time, reverse=True)

    for folder in sorted_folders:
        latest_time = get_latest_mod_time(folder)
        readable_time = datetime.fromtimestamp(latest_time).strftime('%Y-%m-%d %H:%M:%S') if latest_time else 'No files'
        print(f'{folder}: {readable_time}')

print_sorted()
count_blueprints()