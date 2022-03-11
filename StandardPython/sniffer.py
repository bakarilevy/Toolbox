import sys
import getopt
import pcapy
from impacket.ImpactDecoder import EthDecoder


dev = "en0"
filter = "arp"
decoder = EthDecoder()

def handle_packet(data):
    print(decoder.decode(data))

def usage():
    print(f"{sys.argv[0]} -i <device> -f <pcap-filter>")
    sys.exit(1)

def main():
    try:
        cmd_opts = "f:i:"
        opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
    except getopt.GetoptError:
        usage()
    for opt in opts:
        if opt[0] == "-f":
            filter = opt[1]
        elif opt[0] == "-i":
            dev = opt[1]
        else:
            usage()
    # Open device in promiscuous mode
    pcap = pcapy.open_live(dev, 1500, 0, 100)
    # Set pcap filter
    pcap.setfilter(filter)
    # Begin sniffing
    pcap.loop(0, handle_packet)