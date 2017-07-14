#!/usr/bin/env python3
''' Implementation of a nmap scan using nmap.
'''
import argparse
import nmap
from pprint import pprint

def main():
    '''Receives arguments from the command line and passes the output to the
    nmap PortScanner class, performs scan and prints out results to the screen
    '''
    parser = argparse.ArgumentParser(description='''nmap port scanner
                                     implementation''')
    parser.add_argument('-i', '--ip', help='IP address of host to scan',
                        required=True)
    parser.add_argument('-p', '--ports', help='''comma separated list of ports
                        to scan. i.e. 25,80,443''', required=True)
    parser.add_argument('-a', '--argm', help='''Arguments as would be passed
                        to the nmap script. i.e. sV ''', required=True)
    args = parser.parse_args()
    arg_addr = args.ip
    arg_ports = args.ports
    arg_args = '-' + args.argm

    scanner = nmap.PortScanner()
    results = scanner.scan(hosts=arg_addr, ports=arg_ports, arguments=arg_args)
    pprint(results)

if __name__ == '__main__':
    main()
