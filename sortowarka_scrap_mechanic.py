import os
import time
from time import sleep
from datetime import datetime
import pathlib
import shutil


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
def Walkthrough():
    for subdir, dirs, files in os.walk(rootdir):
        print(" ")
        print(subdir)
        for file in files:
            file_path = os.path.join(subdir, file)
            modification_time = os.path.getmtime(file_path)
            readable_time = time.ctime(modification_time)
            print(os.path.join(file, "Last modification time: ", readable_time))

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

def mk_dir():
    directory = "0000Blueprints_work"
    parent_dir = rootdir
    path = os.path.join(parent_dir, directory)
    isExist = os.path.exists(path)
    print(isExist)
    try:
        os.mkdir(path)
    except:
        isExist == True

def move_to_work_folder():
    work_folder = os.path.join(rootdir, "0000Blueprints_work")
    if not os.path.exists(work_folder):
        os.mkdir(work_folder)
    print(f"Work folder location: {work_folder}")

    folders = [os.path.join(rootdir, folder) for folder in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, folder))]
    
    for folder in folders:
        folder_name = os.path.basename(folder)
        if folder_name != "0000Blueprints_work":
            target_path = os.path.join(work_folder, folder_name)
            try:
                shutil.move(folder, target_path)
                print(f"Moved {folder} to {target_path}")

                temp_file_path = os.path.join(target_path, "temp_file.txt")
                with open(temp_file_path, 'w') as temp_file:
                    temp_file.write("") 
                print(f"Created temporary file: {temp_file_path}")

                os.remove(temp_file_path)
                print(f"Deleted temporary file: {temp_file_path}")

            except Exception as e:
                print(f"Failed to move {folder}: {e}")
        sleep(0.25)

def move_back_to_main_folder():
    work_folder = os.path.join(rootdir, "0000Blueprints_work")
    if not os.path.exists(work_folder):
        print(f"Work folder {work_folder} does not exist. Nothing to move.")
        return

    folders = [os.path.join(work_folder, folder) for folder in os.listdir(work_folder) if os.path.isdir(os.path.join(work_folder, folder))]
    sorted_folders = sorted(folders, key=get_latest_mod_time, reverse=True)

    for folder in sorted_folders:
        folder_name = os.path.basename(folder)
        target_path = os.path.join(rootdir, folder_name)
        try:
            shutil.move(folder, target_path)
            print(f"Moved {folder} back to {target_path}")
        except Exception as e:
            print(f"Failed to move {folder}: {e}")
        sleep(0.01)

mk_dir()
Walkthrough()
move_to_work_folder()
move_back_to_main_folder()
print_sorted()
Walkthrough()
count_blueprints()