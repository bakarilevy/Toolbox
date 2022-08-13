#!/usr/bin/python
import os
from scapy.all import *


iface = "wlan0"

os.system("/usr/sbin/iwconfig " + iface + " mode monitor")

# Dump packets that are not beacons, probe request or responses
def dump_packet(packet):
    if not packet.haslayer(Dot11Beacon) and not packet.haslayer(Dot11ProbeReq) and not packet.haslayer(Dot11ProbeResp):
        print(packet.summary())
        if packet.haslayer(Raw):
            print(hexdump(packet.load))
            print("\n")

while True:
    for channel in range(1, 14):
        os.system("/usr/sbin/iwconfig " + iface + " channel " + str(channel))
        print("Sniffing on channel " + str(channel))
        sniff(iface=iface, prn=dump_packet, count=10, timeout=3, store=0)