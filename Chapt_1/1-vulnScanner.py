#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import os
import sys
import timeit
from pympler import tracker

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket()
        s.connect((ip, port))
        print '[+] Connection established %s %s' %(ip, port)
        banner = s.recv(1024)
        print banner
        return banner
    except Exception, excpt:
#        print '[-] Connection failed. %s %s. %s' %(ip, port, excpt)
        return


def checkVulns(banner, filename):

    f = open(filename, 'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print '[+] Server is vulnerable: ' +\
                banner.strip('\n')


def main():

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print '[-] ' + filename +\
                ' does not exist.'
            exit(0)

        if not os.access(filename, os.R_OK):
            print '[-] ' + filename +\
                ' access denied.'
            exit(0)
    else:   
        print '[-] Usage: ' + str(sys.argv[0]) +\
            ' <vuln filename>'
        exit(0)

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()

    portList = [21,22,25,80,110,443]
    for x in range(17, 31):
        ip = '172.28.7.' + str(x)
        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print '[+] ' + ip + ' : ' + banner
                checkVulns(banner, filename)

    t2 = timeit.default_timer()
    print 'Total time to execute was: %s seconds' %(t2-t1)
    tr.print_diff()


if __name__ == '__main__':
    main()
