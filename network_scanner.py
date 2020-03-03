#!/usr/bin/env python

import scapy.all as scapy
import optparse
import subprocess

def getUserInput():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest="ip", help="Specify ip range to scan ex. 10.0.2.1/24")
    parser.add_option('-s', '--timeout', dest="timeout", help="Set timeout for scan. Default is set to 1")
    options = parser.parse_args()[0]

    if not options.ip:
        print('[+] Please specify ip range. Use --help for more info')
    return options

def scan(ip):
    subprocess.call(['clear'])
    print('[+] Scanning network...')
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    if getUserInput().timeout:
        t = int(getUserInput().timeout)
    else:
        t = 1
    answered_list = scapy.srp(arp_req_broadcast, timeout=t, verbose=False)[0]
    client_list = []

    for element in answered_list:
        client = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc
        }
        client_list.append(client)

    subprocess.call(['clear'])
    return client_list


def printRes(list):
    print('IP\t\t\tMAC Address\n------------------------------------------')

    for client in list:
        print(client["ip"] + '\t\t' + client["mac"])

user = getUserInput()

if user.ip:
    printRes(scan(user.ip))
    print('')
    choice = raw_input('Do you want the information to persist in the console? [y/n]:')

    if (choice == 'n' or choice == ''):
        subprocess.call(['clear'])
