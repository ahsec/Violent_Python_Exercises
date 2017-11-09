#!/usr/bin/env python3
'''Script to send knwon malicious packets, for which IDS signatures exist to a
system.  The objective is to verify that existing IDS will alert on this
traffic.
Attacks are taken from Snort rules, found at
https://github.com/eldondev/Snort/blob/master/rules/
'''
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import random
import argparse
import ipaddress

class Attacks(object):
    def __init__(self, ip_dst, iface, count):
        self.ip_dst = ip_dst
        # Random IP address 
        self.ip_src = ".".join(map(str, (random.randint(0, 255)
                                         for _ in range(4))))
        self.iface = iface
        self.count = count
    def ddos_attacks(self):
        """
        alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS TFN Probe";
            icmp_id:678; itype:8; content:"1234"; reference:arachnids,443;
            classtype:attempted-recon; sid:221; rev:4;)
        alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS tfn2k icmp
                possible communication";
             icmp_id:0; itype:0; content:"AAAAAAAAAA";
             reference:arachnids,425; classtype:attempted-dos; sid:222; rev:2;)
        alert udp $EXTERNAL_NET any -> $HOME_NET 31335
            (msg:"DDOS Trin00 Daemon to Master PONG message detected";
            content:"PONG"; reference:arachnids,187;
            classtype:attempted-recon; sid:223; rev:3;)
        alert icmp $EXTERNAL_NET any -> $HOME_NET any
            (msg:"DDOS TFN client command BE"; icmp_id:456; icmp_seq:0;
            itype:0; reference:arachnids,184; classtype:attempted-dos;
            sid:228; rev:3;)
        """
        ip_pkt = IP(src=self.ip_src, dst=self.ip_dst)
        # Building DDOS packets
        ddos_tfn = ip_pkt/ICMP(type=8,id=678)/Raw(load='1234')
        ddos_tfn2k = ip_pkt/ICMP(type=0)/Raw(load='1234')
        ddos_trin00 = ip_pkt/UDP(dport=31335)/Raw(load='PONG')
        ddos_tfn_cl = ip_pkt/ICMP(type=0,id=456)
        ddos_pkts = {
                     'ddos TFN Probe': ddos_tfn,
                     'ddos tfn2k': ddos_tfn2k,
                     'ddos Trin00 Daemon to master': ddos_trin00,
                     'ddos TFN Client Command': ddos_tfn_cl
                    }
        return ddos_pkts
    def linux_attacks(self):
        """
        alert udp $EXTERNAL_NET any -> $HOME_NET 518
            (msg:"EXPLOIT ntalkd x86 Linux overflow";
            content:"|01 03 00 00 00 00 00 01 00 02 02 E8|";
            reference:bugtraq,210; classtype:attempted-admin;
            sid:313; rev:4;)
        alert udp $EXTERNAL_NET any -> $HOME_NET 635
            (msg:"EXPLOIT x86 Linux mountd overflow";
            content:"^|B0 02 89 06 FE C8 89|F|04 B0 06 89|F";
            reference:bugtraq,121; reference:cve,1999-0002;
            classtype:attempted-admin; sid:315; rev:6;)
        """
        ip_pkt = IP(src=self.ip_src, dst=self.ip_dst)
        # Building Linux exploit packets
        ntalkd_x86 = ip_pkt/UDP(dport=518) \
                     /Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
        mountd_oflow = ip_pkt/UDP(dport=635) \
                       /Raw(load="\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89")
        linux_pkts = {
                      'EXPLOIT ntalkd x86 Linux overflow': ntalkd_x86,
                      'EXPLOIT x86 Linux mountd overflow': mountd_oflow
                     }
        return linux_pkts
    def scan_attacks(self):
        """
        alert udp $EXTERNAL_NET any -> $HOME_NET 7
            (msg:"SCAN cybercop udp bomb"; content:"cybercop";
            reference:arachnids,363; classtype:bad-unknown; sid:636; rev:1;)
        alert udp $EXTERNAL_NET any -> $HOME_NET 10080:10081
            (msg:"SCAN Amanda client version request"; content:"Amanda";
            nocase; classtype:attempted-recon; sid:634; rev:2;)
        """
        ip_pkt = IP(src=self.ip_src, dst=self.ip_dst)
        # Building scan packets
        cybercop = ip_pkt/UDP(dport=7)/Raw(load="cybercop")
        amanda = ip_pkt/UDP(dport=10080)/Raw(load="Amanda")
        scan_pkts = {
                     "cybercop": cybercop,
                     "Amanda": amanda
                    }
        return scan_pkts
    def send_pkts(self, pkt_dict):
        # Method to send the packets.
        print("#"*40)
        print("# Attack source: {}".format(self.ip_src))
        print("# Attack Destination: {}".format(self.ip_dst))
        print("#"*40)
        for name, pkt in pkt_dict.items():
            print("Sending attack {} ... Sent".format(name))
            try:
                send(pkt, iface=self.iface, count=self.count)
            except OSError:
                raise SystemExit("Error: Interface {} doesn't exist".format(self.iface))

def main():
    parser = argparse.ArgumentParser(description='''Sends known to be maliciuos
                                     packets in order to trigger IDS
                                     alerts. Source IP address will be
                                     randonmly generated''')
    parser.add_argument('dst', help='Destination IP')
    parser.add_argument('-i', '--iface', help='''Network Interface to send the
                        attacks [eth0]''',default='eth0', required=False)
    parser.add_argument('-c', '--count', help='''Number of packets per attack
                        to send [1]''', default=1, required=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ddos', action="store_true",
                       help='Will send packets to trigger DDoS alerts')
    group.add_argument('--scan', action="store_true",
                       help='Will send packets to trigger scan alerts')
    group.add_argument('--linux', action="store_true",
                       help='Will send packets to trigger linux alerts')
    args = parser.parse_args()
    try:
        ip_dst = str(ipaddress.ip_address(args.dst))
    except ValueError:
        raise SystemExit('Error: Enter a valid IP address')
    try:
        count = int(args.count)
    except ValueError:
        raise SystemExit('Error: Count only accepts numbers')
    iface = args.iface

    attack = Attacks(ip_dst, iface, count)
    if args.ddos:
        pkts = attack.ddos_attacks()
    elif args.scan:
        pkts = attack.scan_attacks()
    else:
        pkts = attack.linux_attacks
    attack.send_pkts(pkts)

if __name__ == '__main__':
    main()
