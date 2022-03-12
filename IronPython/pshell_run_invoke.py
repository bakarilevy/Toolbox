import clr
clr.AddReference("System.Management.Automation")
from System.Management.Automation import RunspaceInvoke


runspace = RunspaceInvoke()
psobjects = runspace.Invoke("Get-Process -Name lssas")
process = psobjects[0]

print("Path = ", process.Properties["Path"].Value)

for prop in process.Properties:
    name = prop.Name
    if name in ("ExitCode", "ExitTime", "StandardIn", "StandardOut", "StandardInput", "StandardOutput", "StandardError"):
        # Can't fetch these on a process that hasn't exited or redirected the in/out/error streams
        continue
    print(prop.Name, prop.Value)