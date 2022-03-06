import wmi

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

def main():
    print("WMI Tool")
    print("Example: RuntimeBroker.exe")
    proc_name = input("Enter exe to search for: ")
    proc_id = get_pid(proc_name)
    print(proc_name)
    print(proc_id)

if __name__=="__main__":
    main()