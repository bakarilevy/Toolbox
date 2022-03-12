import clr
clr.AddReference("System.Management")
from System.Management import ManagementObject
from System.Threading import Thread


query = "Win32_PerfFormattedData_PerfOS_Processor.Name='_total'"
while True:
    mo = ManagementObject(query)
    print(mo["PercentProcessorTime"])
    Thread.CurrentThread.Join(5000)