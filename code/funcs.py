# py-coreutils/funcs.py
# file with funcs used in the rest of scripts

import os
import subprocess

# method to return all the files in a given dir
def get_dir_files(Dir, File) -> tuple:
    for root, dirs, files in os.walk(Dir):
        return files + dirs

# method to remove separator (/) from the end of a directory name and get basename instead of full path
def get_basename(f) -> str:
    return os.path.basename(f.rstrip(os.path.sep))

# method to run a command - handling possible errors
def run(command):
    try:
        subprocess.run(command, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("ERROR", e)
    except Exception as e:
        print("ERROR:", e)

# method to delete files
def delete(File, PROG_NAME, verbose=False):
    command = ["/bin/rm", "-rf", File]
    run(command)
    if verbose: print(f"{PROG_NAME}: deleting -> '{File}'")

# method to move files to trash
def move(File, Dir, PROG_NAME, verbose=False):
    try:
        os.rename(File, Dir)
        if verbose: print(f"{PROG_NAME}: moving '{File}' -> {Dir}")
    except PermissionError:
        print(f"{PROG_NAME}: error: the user doesn't have enough permissions to create the directory '{Dir}'")
        exit(1)

# method to create directories
def mkdir(Dir, PROG_NAME):
    try:
        os.makedirs(Dir, exist_ok=True)    # create dir if doesn't exist
    except PermissionError:
        print(f"{PROG_NAME}: error: the user doesn't have enough permissions to create the directory '{Dir}'")
        exit(1)
    except Exception as e:
        print(f"{PROG_NAME}: error: there was a problem when trying to create the directory '{Dir}'")
        print(f"{PROG_NAME}: error: {e}")
        exit(1)
