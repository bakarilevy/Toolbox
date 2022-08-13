import os


def delete_local_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"{filename} is not in the current folder")