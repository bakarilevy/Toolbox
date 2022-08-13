import clr
clr.AddReference("System.Management")
from System.Management import ManagementObjectSearcher


query = "Select * from Win32_LogicalDisk"
searcher = ManagementObjectSearcher(query)

for drive in searcher.Get():
    for p in drive.Properties:
        print(p.Name, p.Value)
    print()