# The Toolbox

TODO : Experiment with Cython and the httpimport package to dynamically load syscall attacks at runtime

- Recon
- Enumeration
- Exploitation
- Persistence
- Forensics

## Recon

### Finding Emails
hunter.io
phonebook.cz
clearbit (Chrome Extension)

### Breached Credentials
Credential Stuffing

### Hunting Subdomains
crt.sh (This website can be used for certificate fingerprinting)
To use a wildcard on that site for search with the follwoing format:
```
%.target.com
```

We can use the sublist3r tool for domain discovery.
```
sublist3r -d <target.com>
```

OWASP Amass can also be used.

### Geoint
geoguesser

### Email Discovey
Search plaforms:
```
hunter.io
phonebook.cz
clearbit (chrome only)
```
Email verification:
```
verifyemailaddress.io
email-checker.net/validate
```
Don't underestimate "forgot passwords"

### Password Discovery
```
dehashed
weleakinfo
leakcheck
snusbase
haveibeenpwned
scylla.sh
hashes.org
```

### Username Discovery
```
namechk.com
```
### Person Discovery
```
whitepages.com
truepeoplesearch.com
fastpeoplesearch.com
thatsthem.com
pimeye
tineye
```

### Voter Records
```
voterrecords.com
```

## Networking

Shows your different interface types and IP addresses associated with them.
```
ifconfig
```
The newer command to replace ifconfig is now ip
```
ip a (ifconfig)
ip n (arp table)
ip r (routing table)
```
For wireless
```
iwconfig
```
Used to test connectivity between hosts.
```
ping <addr>
```
IP address and MAC address associated with it.
```
arp -a
```
Displays active connections on your machine.
```
netstat -ano
```
Displays routing table along with default gateway.
```
route
```

LM Hash for Pass the Hash attacks on Windows
```
aad3b435b51404eeaad3b435b51404ee
```
To run the SOCKS5 Proxy server simply start the server and try tunneling traffic through it:
```
curl -x socks5://username:password@127.0.0.1:3000 https://httpbin.org/get
```

## StandardPython
Compiling a python binary using nuitka is quite simple
```
python -m nuitka --windows-disable-console --onefile windows.py
```
To solve the error:
```
Nuitka-Scons:INFO: Backend C compiler: gcc (gcc).
collect2: fatal error: ld terminated with signal 11 [Segmentation fault]                              
compilation terminated. Error 1
```
Try running:
```
python3 -m nuitka --lto=no windows.py
```

## Cython

Experimenting with Cython for Win32 API

In the example vector pyx:

```py
# distutils: language=c++


from libcpp.vector cimport vector

def primes(unsigned int nb_primes):
    cdef int n, i
    cdef vector[int] p
    p.reserve(nb_primes) # Allocate memory for "nb_primes" elements
    n = 2
    while p.size() < nb_primes:
        for i in p:
            if n % i == 0:
                break
        else:
            p.push_back(n)
        n += 1
    return p
```
The first line is a compiler directive that tells Cython to compile the code to C++, allowing us to make use of the standard library

We can build this by running the setup.py:
```py
# python setup.py build_ext --inplace
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("vector.pyx", compiler_directives={"language_level" : 3})
)

```

And import and use the module just like any other python module in main.py, keep in mind the built file has been renamed to vector.pyd:
```py
import vector

print(vector.primes(20))
```


## IronPython

Loading .NET Assemblies in memory from Powershell:
```
$directorypath = (Get-Item .).FullName
$assemblypath = $directorypath + "\program.dll"
$bytes = [System.IO.File]::ReadAllBytes($assemblypath)
$assembly = [System.Reflection.Assembly]::Load($bytes)
$entryPointMethod = $assembly.GetTypes().Where({ $_.Name -eq 'Program' }, 'First').GetMethod('Main', [Reflection.BindingFlags] 'Static, Public, NonPublic')
$entryPointMethod.Invoke($null, (, [string[]] ($null)))
```

With pyc.py you can create console or Windows Assemblies from python scripts.
Basic usage looks like this:
```
ipyc /out:myprogram.exe /main:mainfile.py /target.exe program.py support.py
```

To create a standalone executable you will need to compile with the command:
```
ipyc /target:winexe /embed /standalone /main:program.py
```

The above will generate an assembly called myprogram.exe (/out) which is a console app (/target) and will execute the code in mainfile.py first (/main) and will also include code from program.py and support.py in the assembly.

You can also perform static compilation of a .NET assembly using IronPython iteslf:
```py
import clr
# Assembly Name, File names, Key Word Arguments
clr.CompileModules("ipy_modules.dll", "module1.py", "module2.py")
```

Now we can import and use these modules:
```py
import clr
clr.AddReference("ipy_modules.dll")
import module1, module2
```

CompileModules also takes a keyword mainModules argument that specifies the python file that acts as the entry point for the application.

C# Class Library for IronPython example:
```c#
using System;
using System.Collections;

namespace PythonExtension
{
    public delegate int Callback(int input);

    public class PythonClass : IEnumerable //This class implements IEnumerable
    {
        private int _value;
        private Callback _callback;

        public PythonClass(int value, Callback callback) // Constructor takes a callback value
        {
            _value = value;
            _callback = callback;
        }

        public override string ToString() // Used for String representation
        {
            return String.Format("PythonClass<{0}>", _value);
        }

        public IEnumerator GetEnumerator() //Used for Iteration
        {
            for (int i = _value; i > 0; i--)
            {
                if (i % 2 == 0) {
                    yield return callback(i);
                }
            }
        }

        public static PythonClass operator + (PythonClass a, PythonClass, b) // Operator Overloading for addition
        {
            return new PythonClass(a._value + b._value, a.callback);
        }

        public Object this[Object index] {
            get {  // Equivalent of Python __getitem__
                Console.WriteLine("Indexed with {0}", index);
                return index;
            }
            set {  // Equivalent of Python __setitem__
                Console.WriteLine("Index {0} set to {1}", index, value);
            }
        }
    }
}
```

P/Invoke Wrapper:
```c#
using System;
using System.Text;
using System.Runtime.InteropServices;

namespace WindowsUtils
{
    public class WindowsUtils
    {
        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetTopWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindow(IntPtr hWnd, uint wCmd);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowTextLength(IntPtr hWnd);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowText(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetClassName(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);
    }
}
```

Using the dotnet_assembly_compiler.py script you can load the above WindowsUtil class into memory:
```py
import clr
assembly = Generate(source, "WindowsUtils", inMemory=True)
clr.AddReference(assembly)
from WindowsUtils import WindowsUtils
```
We can also do:
```py
assembly = Generate(source, "WindowsUtils", inMemory=True)
WindowsUtils = assembly.WindowsUtils.WindowsUtils
```


### Embedding IronPython

To embed the IronPython Engine into a .NET assembly we need to include the 5 assemblies that come with it:

- Microsoft.Scripting.dll
- Microsoft.Scripting.Core.dll
- IronPython.dll
- IronPython.Modules.dll
- Microsoft.Scripting.ExtensionAttribute.dll

The first two assemblies are part of the Dynamic Language Runtime, the next two are part of IronPython.
The final assembly is used so that .NET projects using .NET 2.0 and 3.0 can use IronPython.
It must be included in the project but does not need to be referenced.
The main entrypoint for apps embedding IronPython is the Python class in the IronPython Hosting namespace.

#### Embedding IronPython script into C# Portable Executable

Setting up an IronPython engine in C#:
```c#
using IronPython.Hosting;

ScriptEngine engine = Python.CreateEngine();
```
The Dynamic Language Runtime supports creating multiple runtimes in a single application, allowing for context execution segmented
from each other.
We need to use both the ScriptSource and ScriptScope APIs from the Hosting API to run a python script.

Execute IronPython code from a string in C#:
```c#
ScriptSource source;
source = engine.CreateScriptFromString(sourceCode, SourceCodeKind.Statements);
ScriptScope scope = engine.CreateScope();
source.Execute(scope);
```

Execute IronPython code from a file in C#:
```c#
ScriptSource source;
source = engine.CreateScriptFromFile(path);
ScriptScope scope = engine.CreateScope();
source.Execute(scope);
```

We can also set the command line arguments for a script like this:
```c#
using IronPython.Runtime;

List argList = new List();
argList.extend(args);
ScriptScope sys = Python.GetSysModule(engine);
sys.SetVariable("argv", argList);
```

We will also need to set the module search path properly for import statements during embedding.
```c#
string filename = "program.py";
string path = Assembly.GetExecutingAssembly().Location;
string rootDir = Directory.GetParent(path).FullName;

List<string> paths = new List<string>();
paths.Add(rootDir);

string path = Environment.GetEnvironmentVariable("IRONPYTHONPATH");
if (path != null && path.Length > 0) {
    string[] items = path.Split(";");
    foreach (string p in items) 
    {if (p.Length > 0) { paths.Add(p); }}
}
engine.SetSearchPaths(paths.ToArray());
```

Lets catch any exceptions from IronPython execution without it being fatal to the C# app:
```c#
try {
    ScriptSource source;
    source = engine.CreateScriptSourceFromFile(path);
    int result = source.ExecuteProgram();
    return result
}

catch (Exception e)
{
    ExceptionOperations eo = engine.GetService<ExceptionOperations>();
    Console.Write(eo.FormatException(e));
    return 1;
}
```

#### Embedding IronPython as a scripting engine in C# Application

Lets begin with getting and setting variables from a scope.

Creating an execution scope C#:
```c#
public class Engine
{
    ScriptEngine _engine;
    ScriptRuntime _runtime;
    CompiledCode _code;
    ScriptScope _scope;

    //_runtime.LoadAssembly(typeof(String).Assembly);

    public class Engine(string source)
    {
        _engine = Python.CreateEngine();
        _runtime = engine.Runtime;
        _scope = _engine.CreateScope();
        _scope.SetVariable("__name__", "__main__");
        
        ScriptSource _script = _engine.CreateScriptFromString(source, SourceCodeKind.Statements);
        _code = _script.Compile();
    }

    public bool Execute()
    {
        try
        {
            _code.Execute(_scope);
            return true;
        }
        catch (Exception e)
        {
            ExceptionOperations eo = _engine.GetService<ExceptionOperations>();
            Console.Write(eo.FormatException(e));
            return false;
        }
    }

    public void SetVariable(string name, object value)
    {
        _scope.SetVariable(name, value);
    }

    public bool TryGetVariable(string name, out result)
    {
        return _scope.TryGetVariable(name, out result);
    }
}
```

Retrieving embedded resource from an assembly:
```c#
static string GetSourceCode()
{
    Assembly assembly = Assembly.GetExecutingAssembly();
    string name = "BasicEmbedding.source_code.py";
    Stream stream = assembly.GetManifestResourceStream(name);
    StreamReader textStreamReader = new StreamReader(stream);
    return textStreamReader.ReadToEnd();
}
```
