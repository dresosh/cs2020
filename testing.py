#!/usr/bin/env python

import optparse
import subprocess
import re

# get user input from terminal
def getArgs():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="interface", help="Specify interface to which you want to change the MAC address to")
    parser.add_option('-m', '--newMac', dest="new_mac", help="Specify new MAC address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface. Use --help for more information')
    elif not options.new_mac:
        parser.error('[-] Please specify a new MAC address. Use --help for more information')
    return options

# change mac address
def changeMac(interface, new_mac):
    print('[] Changing MAC address of ' + interface + ' to ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


# check if mac address was changed
def getMacAddr(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    return re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)

options = getArgs()

changeMac(options.interface, options.new_mac)
current_mac = getMacAddr(options.interface)

if current_mac == options.new_mac:
    print('[+] MAC address was successfully changed to ' + current_mac)
else:
    print('[-] MAC address was not changed')