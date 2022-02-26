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

## Python Programming Language
Compiling a python binary using nuitka is quite simple
```
python -m nuitka --onefile --windows-disable-console --windows-company-name=Microsoft --windows-product-version=0.0.1 windows.py
```

## C Programming Language