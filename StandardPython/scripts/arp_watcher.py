import sys
from scapy.all import sniff, ARP
from signal import signal, SIGINT


IFACE = ""
ARP_WATCHER_FILE = "arp-watcher.txt"
IP_MAC = {}

def sig_int_handler(signum, frame):
    print("Got SIGINT Saving ARP database.")
    try:
        f = open(ARP_WATCHER_FILE, "w")
        for(ip, mac) in IP_MAC.items():
            f.write(f"IP:{ip} MAC:{mac}\n")
            f.close()
            print("Done.")
    except IOError:
        print(f"Cannot write file {ARP_WATCHER_FILE}")
        sys.exit(1)

def watch_arp(packet):
    # Got ARP Response
    if packet[ARP].op == 2:
        print(f"{packet[ARP].hwsrc} {packet[ARP].psrc}")
        # New Device
        if IP_MAC.get(packet[ARP].psrc) == None:
            print(f"Found new device {packet[ARP].hwsrc} {packet[ARP].psrc}")
            IP_MAC[packet[ARP].psrc] = packet[ARP].hwsrc
        # Device has a different IP
        elif IP_MAC.get(packet[ARP].psrc) and IP_MAC[packet[ARP].psrc] != packet[ARP].hwsrc:
            print(f"{packet[ARP].hwsrc} has new IP: {packet[ARP].psrc}")

def main():
    IFACE = input("Please enter an interface to sniff traffic on: ")
    signal(SIGINT, sig_int_handler)
    try:
        sniff(prn=watch_arp, filter="arp", iface=IFACE, store=0)
    except Exception as e:
        print(f"Error attempting to conduct attack: {e}")
    

if __name__ == "__main__":
    main()