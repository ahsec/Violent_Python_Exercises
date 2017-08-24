#!/usr/bin/env python3
''' Script that returns the Geo Location of a given IP address by using the
http://ipinfodb.com/ service.
A key (provided on a separate file is required.
'''
import urllib3
import argparse

def get_key(fname):
    '''Retrieves the first line of the provided filename after removing
    the return carriage character.
    '''
    with open(fname, 'r') as fopen:
        key = fopen.readline()
        return key.strip('\r\n')

def get_ipgeo(key, ip):
    '''Uses urllib to query the ipinfodb service and obtain a Geo Location of
    the provided IP address.
    '''
    url = 'http://api.ipinfodb.com/v3/ip-city/?key={}&ip={}'.format(key, ip)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return str(response.data)

def main():
    '''Argument parsing and assigning variables.
    '''
    parser = argparse.ArgumentParser(description='''Retrieves the Geolocation
                                      of a given IP address by querying
                                      ipinfodb.com. A service key is necessary
                                      ''')
    parser.add_argument('-k', '--key', help='File containing the service key',
                        required=True)
    parser.add_argument('-i', '--ip', help='IP Address to obtain location for',
                        required=True)
    args = parser.parse_args()
    fname = args.key
    ip = args.ip

    key = get_key(fname)
    location = get_ipgeo(key, ip)
    status, _, ip_addr, country_code, country, state, city, zip_code, lat, longt, timez = location.split(';')
    if country == '-':
        raise SystemExit("IP Address {} not in ipinfodb Database".format(ip))
    print(country, state, city)

if __name__ == '__main__':
    main()
