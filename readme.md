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
