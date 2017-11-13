#!/usr/bin/env python
''' Downloads images from a provided website and extracts the metadata from
the downloaded images.
'''
import argparse
import urlparse
import ImageDownloader
from PIL import Image
from os import listdir
from pprint import pprint
from os.path import isfile, join
from PIL.ExifTags import TAGS

def get_gps_img(img_files):
    '''Given a list of filenames. Returns a list of files that contain GPS
    information.'''
    gps_imgs = []
    for img_file in img_files:
        img_info = {}
        imgfile = Image.open(img_file)
        try:
            info = imgfile._getexif()
        except AttributeError:
            continue
        else:
            if info:
                for key, value in info.items():
                    decoded = TAGS.get(key, key)
                    img_info[decoded] = value
                    if img_info.get('GPSInfo'):
                        gps_imgs.append(img_file)
                        break
    return gps_imgs

def main():
    parser = argparse.ArgumentParser(description='''Downloads images from a
                                     provided URL and extracts the metadata
                                     from those images.''')
    parser.add_argument('-u', '--url', help='URL to download images from',
                        required=True)
    parser.add_argument('-o', '--out', help='''Directory to write the images
                        to''')
    args = parser.parse_args()
    rootUrl = args.url
    downloadLocationPath = args.out
    maxRecursionDepth = 0
    minImageFileSize = long(1)

    netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
    website = netloc[-2] + netloc[-1]
    print('[+] Downloading Image files from %s'%(rootUrl))
    images = ImageDownloader.ImageWebsite(rootUrl, maxRecursionDepth,
                                          minImageFileSize,
                                          downloadLocationPath, website)
    img_files = [join(downloadLocationPath, f) for f in listdir(downloadLocationPath) if
                 isfile(join(downloadLocationPath, f))]
    gps_imgs = get_gps_img(img_files)
    print('\n\n' + '*-' * 7 + ' Image Metadata Analysis ' + '*-' * 7)
    print('[!] Images with GPS Info:')
    pprint(gps_imgs)

if __name__ == '__main__':
    main()
