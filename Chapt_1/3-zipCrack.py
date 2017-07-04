#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile
import optparse
from threading import Thread

import timeit
from pympler import tracker

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print '[+] Found password ' + password + '\n'
    except:
        pass


def main():
    parser = optparse.OptionParser("usage %prog "+\
      "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',\
      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
      help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print parser.usage
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()

    t2 = timeit.default_timer()
    tr.print_diff()
    print 'Total time to execute: %s seconds' %(t2-t1)

if __name__ == '__main__':
    main()
