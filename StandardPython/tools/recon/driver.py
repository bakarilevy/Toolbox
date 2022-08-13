import os
import time
import nmap
from configparser import ConfigParser


red = '\033[31m' #red
blue = '\033[34m' #blue
green = '\033[32m' #green
yellow = '\033[33m' #yellow
magenta = '\033[34m' #magenta
cyan = '\033[36m' #cyan
endline = '\033[0m' #end

class DriverMain():
    """
	Objective :
	This class only takes user input for CLI mode and verifies whether the supplied input
	is proper and if it is, control is passed onto the nmap processor, requires python-nmap library.
	"""

    def __init__(self, nmap_scan):
        # Pass an NmapScan object on construction
        self.NmapScanObj = nmap_scan
    
    def prompt_scan_type(self):
        # Confirm if user wants to launch a new scan or continue a prior scan
        while True:
            scanType = input("Enter a value: \n(1) Launch a new scan \n(2) Continue a previous scan" + endline)
            try:
                if((scanType == "1") or (scanType == "2")):
                    break
                else:
                    print("Invalid choice")
            except:
                return "1"
            return scanType

    def seperator(self):
        print(red + "-------------------------------------" + endline)

    def prompt_project(self):
        # Get project name

        projectName = input(blue + "What is the name of your project? Please do not use whitespaces: \n" + yellow)
        return projectName

