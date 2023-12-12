# py-coreutils/funcs.py
# file with funcs used in the rest of scripts

# TODO: implement list_files function
# TODO: implement recover function

import os
import sys
import subprocess

# methods to print usage
def print_mvv3_usage():
    print("USAGE: mvv3 --move | -m | --copy | -c SOURCE/s DESTINATION")

# methods to get the size given file (will assume valid files/dirs are passed)
def get_filesize(f) -> int:
    return os.path.getsize(f)/(1024**2) # convert bytes to megabytes

def get_dirsize(d) -> int:
    dir_size = 0
    for root, dirs, files in os.walk(d):
        for f in files:
            full_file_path = os.path.join(root, f)
            dir_size += get_filesize(full_file_path)
    return dir_size

def get_size(f) -> int:
    if os.path.isdir(f):
        return get_dirsize(f)
    elif os.path.isfile(f):
        return get_filesize(f)

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
        sys.exit(1)

# method to create directories
def create_dir(Dir, PROG_NAME):
    try:
        os.makedirs(Dir, exist_ok=True)    # create dir if doesn't exist
    except PermissionError:
        print(f"{PROG_NAME}: error: the user doesn't have enough permissions to create the directory '{Dir}'")
        sys.exit(1)
    except Exception as e:
        print(f"{PROG_NAME}: error: there was a problem when trying to create the directory '{Dir}'")
        print(f"{PROG_NAME}: error: {e}")
        sys.exit(1)

# method to look from a given file in a given dir
def list_files(Dir, File='__show_all__'):
    # TODO: show message if Dir is empty
    for root, dirs, files in os.walk(Dir):
        for f in files:
            if File in f or File == '__show_all__':
                # handle naming
                tmp = f.rsplit('.trash')[0] # remove .trash extension
                file_name, date = tmp.rsplit('%_%')
                print(f'{file_name} removed at -> {date}')

# method to recover file from trash dir
def recover(Dir, File, verbose=False):
    pass
