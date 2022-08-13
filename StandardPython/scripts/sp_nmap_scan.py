#! /usr/bin/python3
import os
import subprocess as sp


class NmapPy():
    def __init__(self, command=[]):
        self.command = command

    def scan(self):
        try:
            p = sp.Popen(self.command, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
            out, err = p.communicate()
            print("\n Nmap scan is complete: ")
            print(f"{out.decode()}")
            print(f"{err.decode()}")
        except Exception as e:
            print(f"Exception caught: {str(e)}")

def main():
    try:
        host = input("[*] Please enter a host to scan: ")
        print("[+] Runnning Nmap Scan")
        nmap = NmapPy(["nmap", "-Pn", "-sV", host])
        nmap.scan()
    except KeyboardInterrupt:
        print("[!] Received exit command, exiting...")
        os._exit()

if __name__=='__main__':
    main()