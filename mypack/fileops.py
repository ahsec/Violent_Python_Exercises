#!/usr/bin/env python3
'''
This module contains functions and classes to perform file operations.
such as reading, writing.
'''

class FileReader(object):
    '''This class attempts to take advantage of generators in order to
    perform efficient operations on file descriptors.
    '''
    def __init__(self, fname, mode='rt'):
        ''' The default mode is reading in text mode.
        '''
        self.fname = fname
        self.mode = mode
    def __iter__(self):
        '''Iter method in order to use in loops.
        '''
        with open(self.fname, self.mode) as fopen:
            for line in fopen:
                yield line.strip('\n')

def main():
    '''
    Foo main.
    '''

if __name__ == '__main__':
    main()
