#!/usr/bin/env python

import subprocess
import optparse
import re

def getArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address")
    parser.add_option("-m", "--newMac", dest="new_mac", help="New MAC address")
    (options, args) = parser.parse_args()
    if not options. interface:
        parser.error('[-] Please specify an interface. Use --help for more info')
    elif not options.new_mac:
        parser.error('[-] Please specify a MAC address, Use --help for more info')
    return options

def changeMac(interface, new_mac):
    print('[+] Changing mac address for ' + interface + ' to ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

def getCurrentMac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_resutl = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_resutl:
        return mac_address_resutl.group(0)
    else:
        print('[-] Could not read MAC address')


options = getArguments()
changeMac(options.interface, options.new_mac)

current_mac = getCurrentMac(options.interface)

if current_mac == options.new_mac:
    print('[+] MAC address was successfully changed to ' + current_mac)
else:
    print('[-] MAC address did not change')

