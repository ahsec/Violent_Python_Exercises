#!/usr/bin/env python3
''' Attempts to perform a Bruteforce attack on a shadow file.
'''
import sys
import crypt
import timeit
from pympler import tracker
import argparse
sys.path.append('../')
import mypack.fileops as fileops

def get_user_hash(shadow_line):
    (user, hashed, *rest) = shadow_line.split(':')
    try:
        (userid, alg, salt, hash_pwd) = ((user,) + tuple(hashed.split('$')[1:]))
    except ValueError:
        '''Couldn't unpack content of hashed because user has * instead of
        passwd, which means that the account is disabled'''
        (userid, hash_pwd) = (user, '*')
    return (userid, hash_pwd)

def main():
    parser = argparse.ArgumentParser(description='''Bruteforcer for *NIX
                                               shadow files''')
    parser.add_argument('-s', '--shad', help='Shadow file to read from',
                       required=True)
    parser.add_argument('-d', '--dict', help='Dictionary file to use',
                        required=True)
    args = parser.parse_args()
    fname_shd = args.shad
    fname_dict = args.dict

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()

    dict_lines = fileops.FileReader(fname_dict)
    shadow_lines = fileops.FileReader(fname_shd)
    user_hash = (get_user_hash(shadow_line) for shadow_line in shadow_lines)
    for userid, hash_pwd in user_hash:
        if hash_pwd == '*':
            print("[-] User {}. Doesn't have a password set.".format(userid))
            break
        for dict_line in dict_lines:
            if crypt.crypt(dict_line, hash_pwd) == hash_pwd:
                print('[+] Recovered, userid {} password {}'.format(userid, dict_line))
                break

    t2 = timeit.default_timer()
    tr.print_diff()
    print('Total time to execute: {} seconds'.format(t2-t1))

if __name__ == '__main__':
    main()
