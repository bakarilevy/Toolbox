import ctypes
import win32con #part of pywin32
from ctypes import wintypes
import psutil

# Win32 Kernel32 API
api = ctypes.windll.kernel32

# Map Functions
CreateToolhelp32Snapshot = api.CreateToolhelp32Snapshot
OpenProcess = api.OpenProcess
CloseHandle = api.CloseHandle
VirtualProtectEx = api.VirtualProtectEx
WriteProcessMemory = api.WriteProcessMemory
ReadProcessMemory = api.ReadProcessMemory
Module32First = api.Module32First
Module32Next = api.Module32Next
Process32First = api.Process32First
Process32Next = api.Process32Next

# Constants & Structures
PROCESS_ALL_ACCESS = win32con.PROCESS_ALL_ACCESS
PAGE_EXECUTE_READWRITE = win32con.PAGE_EXECUTE_READWRITE
TH32CS_SNAPPROCESS = 0x2
TH32CS_SNAPMODULE = 0x8
TH32CS_SNAPMODULE32 = 0x10
INVALID_HANDLE_VALUE = -1

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [('dwSize' , ctypes.wintypes.DWORD),
                ('cntUsage' , ctypes.wintypes.DWORD),
                ('th32ProcessID', ctypes.wintypes.DWORD),
                ('th32DefaultHeapID', ctypes.POINTER(ctypes.wintypes.ULONG)),
                ('th32ModuleID', ctypes.wintypes.DWORD),
                ('cntThreads', ctypes.wintypes.DWORD),
                ('th32ParentProcessID', ctypes.wintypes.DWORD),
                ('pcPriClassBase', ctypes.wintypes.LONG),
                ('dwFlags', ctypes.wintypes.DWORD),
                ('szExeFile', ctypes.c_char * 260)]

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', ctypes.wintypes.DWORD),
                ('th32ModuleID', ctypes.wintypes.DWORD),
                ('th32ProcessID', ctypes.wintypes.DWORD),
                ('GlblcntUsage', ctypes.wintypes.DWORD),
                ('ProccntUsage', ctypes.wintypes.DWORD),
                ('modBaseAddr', ctypes.POINTER(ctypes.wintypes.BYTE)),
                ('modBaseSize', ctypes.wintypes.DWORD),
                ('hModule', ctypes.wintypes.HMODULE),
                ('szModule', ctypes.c_char * 256),
                ('szExePath', ctypes.c_char * 260)]

def GetProcId(processName):
    procId = None
    hSnap = winapi.CreateToolhelp32Snapshot(winapi.TH32CS_SNAPPROCESS, 0)

    if (hSnap != winapi.INVALID_HANDLE_VALUE):
        procEntry = winapi.PROCESSENTRY32()
        procEntry.dwSize = ctypes.sizeof(winapi.PROCESSENTRY32)

        if (winapi.Process32First(hSnap, ctypes.byref(procEntry))):
            # Do While loops do not exist in Python, to emulate this logic we will use a nested function.
            def processCmp(procEntry):
                if (procEntry.szExeFile.decode("utf-8") == processName):
                    nonlocal procId
                    procId = int(procEntry.th32ProcessID)

            processCmp(procEntry)
            while (winapi.Process32Next(hSnap, ctypes.byref(procEntry))):
                processCmp(procEntry)

    winapi.CloseHandle(hSnap)
    return(procId)

def GetModuleBaseAddress(pid, moduleName):
    baseAddress = None
    hSnap = winapi.CreateToolhelp32Snapshot(winapi.TH32CS_SNAPMODULE | winapi.TH32CS_SNAPMODULE32, pid)

    if (hSnap != winapi.INVALID_HANDLE_VALUE):
        modEntry = winapi.MODULEENTRY32()
        modEntry.dwSize = ctypes.sizeof(winapi.MODULEENTRY32)

        if (winapi.Module32First(hSnap, ctypes.byref(modEntry))):
            # Do While loops do not exist in Python, to emulate this logic we will use a nested function.
            def moduleCmp(modEntry):
                if (modEntry.szModule.decode("utf-8") == moduleName):
                    nonlocal baseAddress
                    baseAddress = int(hex(ctypes.addressof(modEntry.modBaseAddr.contents)), 16)

            moduleCmp(modEntry)
            while (winapi.Module32Next(hSnap, ctypes.byref(modEntry))):
                moduleCmp(modEntry)

    winapi.CloseHandle(hSnap)
    return(baseAddress)

def FindDMAAddy(hProc, base, offsets, arch=64):
    size=8
    if (arch == 32): size = 4

    address = ctypes.c_uint64(base)

    for offset in offsets:
        winapi.ReadProcessMemory(hProc, address, ctypes.byref(address), size, 0)
        address = ctypes.c_uint64(address.value + offset)

    return(address.value)

def patchBytes(handle, src, destination, size):
    src = bytes.fromhex(src)
    size = ctypes.c_size_t(size)
    destination = ctypes.c_ulonglong(destination)
    oldProtect = ctypes.wintypes.DWORD()

    winapi.VirtualProtectEx(handle, destination, size, winapi.PAGE_EXECUTE_READWRITE, ctypes.byref(oldProtect))
    winapi.WriteProcessMemory(handle, destination, src, size, None)
    winapi.VirtualProtectEx(handle, destination, size, oldProtect, ctypes.byref(oldProtect))

def nopBytes(handle, destination, size):
    hexString = ""

    for i in range(size):
        hexString += "90"

    patchBytes(handle, hexString, destination, size)

def getPid(name):
    for process in psutil.process_iter():
        try:
            if name == process.name():
                return(process.pid)
        except: pass

def printError(desc=""):
    print(desc + str(ctypes.get_last_error()))

def nativeInject(dllPath, pid):
    # Open handle to target process.
    handle = wintypes.HANDLE(
        winapi.OpenProcess(winapi.PROCESS_ALL_ACCESS, wintypes.BOOL(0), wintypes.DWORD(pid))
    )

    # Allocate space for DLL path string.
    dllPathAddress = wintypes.LPVOID(
        winapi.VirtualAllocEx(handle, winapi.NULL, (len(dllPath) + 1), winapi.MEM_RESERVE | winapi.MEM_COMMIT, winapi.PAGE_EXECUTE_READWRITE)
    )

    if (dllPathAddress.value != None):
        # Write path to memory.
        pathWritten = wintypes.BOOL(
            winapi.WriteProcessMemory(handle, dllPathAddress, dllPath, len(dllPath), winapi.NULL)
        )
        if (pathWritten.value):
            # Create remote thread.
            remoteThread = wintypes.HANDLE(
                winapi.CreateRemoteThread(handle, winapi.NULL, winapi.NULL, winapi.LoadLibraryA, dllPathAddress, wintypes.DWORD(0), winapi.NULL)
            )
            if (remoteThread.value == None):
                printError("Error RThread: ")
        else:
            printError("Error Write: ")
    else:
        printError("Error Alloc: ")

    # Close handle.
    winapi.CloseHandle(handle)

def runCode(pid, codeString):
    # Find module base and add relative addresses.
    base = utility.modBase(pid, 'python39.dll')

    # Map functions to addresses.
    Py_InitializeEx = base + 0x00254e60
    PyRun_SimpleString = base + 0x0027b8b0

    # Open handle.
    handle = wintypes.HANDLE (
        winapi.OpenProcess(winapi.PROCESS_ALL_ACCESS, 0, wintypes.DWORD(pid))
    )

    # Py_InitializeEx(0)
    pyinit = wintypes.HANDLE (
        winapi.CreateRemoteThread(handle, None, 0, Py_InitializeEx, 0, 0, None)
    )
    winapi.WaitForSingleObject(pyinit, wintypes.DWORD(10000))

    # Write code to target process.
    codeString = codeString.encode('utf-8') + b'\x00'
    codeAddress = wintypes.LPVOID (
        winapi.VirtualAllocEx(handle, winapi.NULL, (len(codeString) + 1), winapi.MEM_RESERVE | winapi.MEM_COMMIT, winapi.PAGE_EXECUTE_READWRITE)
    )
    if (codeAddress.value != None):
        codeWritten = wintypes.BOOL(
            winapi.WriteProcessMemory(handle, codeAddress, codeString, len(codeString), winapi.NULL)
        )
        if (codeWritten.value):
            # PyRun_SimpleString(codeAddress)
            winapi.CreateRemoteThread(handle, None, 0, PyRun_SimpleString, codeAddress, 0, None)
    winapi.CloseHandle(handle)

def loadCode(path):
    return(open(path).read())

# Call injector.getPid to get target pid.
pid = utility.getPid('ac_client.exe')

if (pid != None):
    # Call injector.inject to inject interpreter into target.
    injector.inject(b'<DLL PATH>', pid)

    # Call loadCode to get code string.
    codeString = loadCode('<CODE PATH>')

    # Call runCode with code string.
    runCode(pid, codeString)

dllPath = b"<DLL PATH>"
inject(dllPath, <PROCESS PID>)

pid = getPid("ac_client.exe")

# Get PID, open handle, get module address.
pid = utility.GetProcId("ac_client.exe")
handle = winapi.OpenProcess(winapi.PROCESS_ALL_ACCESS, 0, ctypes.wintypes.DWORD(pid))
moduleAddress = utility.GetModuleBaseAddress(pid, "ac_client.exe")

# Write over the bytes which decrement ammo.
ammoDecAddress = moduleAddress + 0x637E9
utility.nopBytes(handle, ammoDecAddress, 2)

# Resolve current ammo pointer chain, write to current ammo value.
curAmmoBase = moduleAddress + 0x0010F418
ammoAddress = utility.FindDMAAddy(handle, curAmmoBase, [0x58, 0x1E8, 0x84, 0x14], 32)
winapi.WriteProcessMemory(handle, ammoAddress, ctypes.byref(ctypes.c_int(1337)), ctypes.sizeof(ctypes.c_int), None)
winapi.CloseHandle(handle)

