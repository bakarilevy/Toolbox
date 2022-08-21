# I converted this based on Minidump https://github.com/3xpl01tc0d3r/Minidump/
import clrtype
import System
import System.Text as Text
import System.Collections.Generic as Generic
import System.Threading.Tasks as ThreadTasks
import System.Runtime.InteropServices as InterOp
import System.IO as IO
import System.Diagnostics  as Diagnostics
import System.Security.Principal as Principal
from System.Runtime.InteropServices import DllImportAttribute, PreserveSigAttribute, Marshal, HandleRef
from Microsoft.Win32.SafeHandles import SafeFileHandle


class MINIDUMP_TYPE:
    MiniDumpNormal = 0x00000000
    MiniDumpWithDataSegs = 0x00000001
    MiniDumpWithFullMemory = 0x00000002
    MiniDumpWithHandleData = 0x00000004
    MiniDumpFilterMemory = 0x00000008
    MiniDumpScanMemory = 0x00000010
    MiniDumpWithUnloadedModules = 0x00000020
    MiniDumpWithIndirectlyReferencedMemory = 0x00000040
    MiniDumpFilterModulePaths = 0x00000080
    MiniDumpWithProcessThreadData = 0x00000100
    MiniDumpWithPrivateReadWriteMemory = 0x00000200
    MiniDumpWithoutOptionalData = 0x00000400
    MiniDumpWithFullMemoryInfo = 0x00000800
    MiniDumpWithThreadInfo = 0x00001000
    MiniDumpWithCodeSegs = 0x00002000

class NativeMethods(object):
    __metaclass__ = clrtype.ClrClass
    DllImport = clrtype.attribute(DllImportAttribute)
    PreserveSig = clrtype.attribute(PreserveSigAttribute)

    @staticmethod
    @DllImport("dbghelp.dll", SetLastError= True)
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.UInt64, InterOp.SafeHandle, System.UInt64, System.IntPtr, System.IntPtr, System.IntPtr)
    @clrtype.returns(bool)
    def MiniDumpWriteDump(hProcess, processId, hFile, dumpType, expParam, userStreamParam, callbackParam): raise NotImplementedError("MinidumpWriteDump not found.")

def Dump(processHandle, processId, processName):
    '''
    Accepts:
        processHandle: System.IntPtr
        processId: System.UInt64
        processName: str
    returns:
        void
    '''
    try:
        filename = processName + "_" + str(processId) + ".dmp"
        fs = IO.FileStream(filename, IO.FileMode.Create, IO.FileAccess.ReadWrite, IO.FileShare.Write)
        status = NativeMethods.MiniDumpWriteDump(processHandle, processId, fs.SafeFileHandle, MINIDUMP_TYPE.MiniDumpNormal, System.IntPtr.Zero, System.IntPtr.Zero, System.IntPtr.Zero)
        
        if status:
            print("Process was dumped successfully")
        else:
            print("Cannot dump selected process")
    except Exception as e:
        print("Error during execution: " + e.ToString())

def main():
    identity = Principal.WindowsIdentity.GetCurrent()
    principal = Principal.WindowsPrincipal(identity)
    if(principal.IsInRole(Principal.WindowsBuiltInRole.Administrator)):
        print("Process running with " + principal.Identity.Name + " privileges with HIGH integrity")
    else:
        print("Process running with " + principal.Identity.Name + " privileges with MEDIUM/LOW integrity")
    proc_name = raw_input("Please enter a process by name: ")
    processes = Diagnostics.Process.GetProcessesByName(proc_name)
    if processes.Length > 0:
        for process in processes:
            print("Dumping " + process.ProcessName + " process")
            print(process.ProcessName + " : Process Handle: " + str(process.Handle))
            print(process.ProcessName + ": Process ID: " + str(process.Id))
            Dump(process.Handle, System.UInt32(process.Id), process.ProcessName)
    else:
        print("Selected process is not running.")

if __name__=='__main__':
    main()