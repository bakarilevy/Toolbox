import clr
clr.AddReference("System.Management")
from System.Management import (
    WqlEventQuery, ManagementEventWatcher
)
from System import TimeSpan
from System.Threading import Thread


timeout = TimeSpan(0, 0, 1)
query = WqlEventQuery("__InstanceCreationEvent", timeout, 'TargetInstance isa "Win32_Process"')
watcher = ManagementEventWatcher()
watcher.Query = query

def arrived(sender, event):
    print("Event arrived")
    real_event = event.NewEvent
    instance = real_event["TargetInstance"]
    for entry in instance.Properties:
        print(entry.Name, entry.Value)
    watcher.EventArrived += arrived
    watcher.Start()
    while True:
        Thread.CurrentThread.Join(1000)
