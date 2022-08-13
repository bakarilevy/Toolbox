import os
import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def main():
    try:
        start_address = input("Please enter a starting IP Address: ")
        end_address = input("Please enter the ending IP Address: ")

        livehosts = []
        ipregex = r"^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"

        if(re.match(ipregex, start_address) is None):
            print("Starting IP address is invalid.")
            os._quit()
        if(re.match(ipregex, end_address) is None):
            print("Ending IP Address is invalid.")
            os._quit()

        first_ip_list = start_address.split(".")
        second_ip_list = end_address.split(".")

        if not (first_ip_list[0]==second_ip_list[0] and first_ip_list[1]==second_ip_list[1] and first_ip_list[2] == second_ip_list[2]):
            print("IP Addresses are not in the same class C subnet")
            os._quit()
        
        if(first_ip_list[3] > second_ip_list[3]):
            print("Starting IP address is greater than ending IP address")
            os._quit()

        networkaddr = first_ip_list[0] + "." + first_ip_list[1] + "." + first_ip_list[2] + "."

        start_ip_last_octet = int(first_ip_list[3])
        end_ip_last_octet = int(second_ip_list[3])

        if (start_ip_last_octet < end_ip_last_octet):
            print(f"Pinging range: {networkaddr + str(start_ip_last_octet)} - {str(end_ip_last_octet)}")
        else:
            print(f"Pinging {networkaddr + str(start_ip_last_octet)}")
        
        for x in range(start_ip_last_octet, end_ip_last_octet):
            packet = IP(dst=networkaddr + str(x))/ICMP()
            response = sr1(packet, timeout=2, verbose=0)
            if not (response is None):
                if(response[ICMP].type == 0):
                    livehosts.append(networkaddr + str(x))
        
        print("Scan complete")
        if len(livehosts) > 0:
            print("Discovered hosts")
            for host in livehosts:
                print(host)
        else:
            print("No live hosts found")
    except KeyboardInterrupt:
        print("Received exit command, exiting...")
        os._quit()

if __name__=='__main__':
    main()