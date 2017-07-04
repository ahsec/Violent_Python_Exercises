#!/usr/bin/env python3
'''Performs a dictionary attack on a password protected zip file.
'''
import argparse
import zipfile
import sys
from threading import Thread
import timeit
from pympler import tracker

sys.path.append('../')
import mypack.fileops as fileops

def extract_zip(zfile, password):
    try:
        zfile.extractall(pwd=str.encode(password))
    except RuntimeError:
        pass
    except FileExistsError:
        pass
    else:
        print('ZIP file extracted with password: {}'.format(password))

def main():
    parser = argparse.ArgumentParser(description='''Performs a dictionary
                                                    attack on a password
                                                    protected zip file.''')
    parser.add_argument('-z', '--zip', help='Password protected ZIP file.',
                        required=True)
    parser.add_argument('-d', '--dic', help='Dictionary file.', required=True)
    args = parser.parse_args()
    fname_zip = args.zip
    fname_dic = args.dic

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()

    passwords = fileops.FileReader(fname_dic)
    zfile = zipfile.ZipFile(fname_zip)
    for password in passwords:
#        try:
        t = Thread(target=extract_zip, args=(zfile, password))
        t.start()
#            zfile.extractall(pwd=str.encode(password))
#        except RuntimeError:
#            pass
#        else:
#            print('ZIP file extracted with password: {}'.format(password))

    t2 = timeit.default_timer()
    tr.print_diff()
    print('Total time to execute: {} seconds'.format(t2-t1))


if __name__ == '__main__':
    main()
