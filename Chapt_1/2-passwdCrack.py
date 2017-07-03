#!/usr/bin/python
# -*- coding: utf-8 -*-
import crypt
import timeit
from pympler import tracker

def testPass(cryptPass):
    salt = cryptPass[0:2]
    dictFile = open('500-worst-passwords.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        if cryptWord == cryptPass:
            print '[+] Found Password: ' + word + '\n'
            return
    print '[-] Password Not Found.\n'
    return


def main():

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()

    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ':' in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print '[*] Cracking Password For: ' + user
            testPass(cryptPass)

    t2 = timeit.default_timer()
    tr.print_diff()
    print('Total time to execute: {} seconds'.format(t2-t1))


if __name__ == '__main__':
    main()
