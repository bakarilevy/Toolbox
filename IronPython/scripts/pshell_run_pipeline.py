import clr
clr.AddReference("System.Management.Automation")
from System.Management.Automation.Runspaces import (
    RunspaceFactory
)


runspace = RunspaceFactory.CreateRunspace()
runspace.Open()

runspace.SessionStateProxy.SetVariable("processName", "ipy")
pipeline = runspace.CreatePipeline()
pipeline.Commands.AddScript("Get-Process -Name $processName")
pipeline.Commands.Add("Out-String")

results = pipeline.Invoke()
for result in results:
    print(result)