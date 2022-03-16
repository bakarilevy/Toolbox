# The Toolbox

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

## Networking Commands

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

You can try to kill the Windows Defender process MsMpEng.exe

## StandardPython
Compiling a python binary using nuitka is quite simple
```
python -m nuitka --onefile windows.py
```

## IronPython
With pyc.py you can create console or Windows Assemblies from python scripts.
Basic usage looks like this:
```
ipyc /out:myprogram.exe /main:mainfile.py /target.exe program.py support.py
```

The above will generate an assembly called myprogram.exe (/out) which is a console app (/target) and will execute the code in mainfile.py first (/main) and will also include code from program.py and support.py in the assembly.

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