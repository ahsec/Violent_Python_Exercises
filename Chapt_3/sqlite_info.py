#!/usr/bin/env python3
'''
This script extracts information about the cookies.sqlite file and 
presents its contents to the screen
This script applies to mozilla firefox file: cookies.sqlite
'''
import os
import sqlite3
import argparse
import itertools
from pprint import pprint

def get_sqlite(fname):
    '''Read from sqlite3 file and return content in the form of a dictionary
    '''
    conn = sqlite3.connect(fname)
    cur = conn.cursor()

    table_names = [row for row in cur.execute("""SELECT name FROM sqlite_master
                                              WHERE type='table';""")]
    for table_name in table_names:
        table = table_name[0]
        query = "PRAGMA table_info('{}')".format(table)
        column_names = [row[1] for row in cur.execute(query)]

        rows = cur.execute("SELECT * FROM '{}';".format(table))
        for row in rows:
            yield dict(itertools.zip_longest(column_names, row))

def main():
    '''Argument parsing and making function calls to retrieve dictionary
    content.
    '''
    parser = argparse.ArgumentParser(description="""Mozilla Firefox file
                                     cookies.sqlite reader.""")
    parser.add_argument('-f', '--file', help='File path for cookies.sqlite',
                        required=True)
    args = parser.parse_args()
    fname = args.file

    if not os.path.isfile(fname):
        raise SystemExit("sqlite file doesn't exist")

    content = get_sqlite(fname)
    for line in content:
        print(line)

if __name__ == '__main__':
    main()

'''
Getting the table name(s)
>>> for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
...   print(row)

Getting the table colunm names
>>> for row in cur.execute("PRAGMA table_info('moz_cookies')"):
...   print(row)

Getting table content (all columns)
>>> for row in cur.execute("SELECT * FROM 'moz_cookies';"):
...   print(row)

'''


