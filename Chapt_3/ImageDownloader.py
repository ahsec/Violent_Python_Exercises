import os
import urllib2
import urlparse
import argparse
from os.path import basename
from BeautifulSoup import BeautifulSoup

#urlList = []

class ImageWebsite(object):
    ''' Website that contains images to be downloaded.
    By calling the init method 
    '''
    def __init__(self, rootUrl, maxRecursionDepth, minImageFileSize, downloadLocationPath, website):
        '''Init method.
        '''
        self.urlList = []
        self.rootUrl = rootUrl
        self.maxRecursionDepth = maxRecursionDepth
        self.minImageFileSize = minImageFileSize
        self.downloadLocationPath = downloadLocationPath
        self.website = website
        self.hdr = {'User-Agent': 'Mozilla/5.0'}

        self.download_images()

        while self.maxRecursionDepth > 0:
            linkTags = self.soup.findAll('a')
            if linkTags:
                for linkTag in linkTags:
                    try:
                        self.rootUrl = linkTag['href']
                        self.maxRecursionDepth = self.maxRecursionDepth - 1
                        self.download_images()
                    except Exception, e:
                        raise SystemExit(e)
            self.maxRecursionDepth = self.maxRecursionDepth - 1

        # call METHOD DOWNLOAD IMAGES,
        # CHECK LEVEL, IF NECESSARY, CALL DOWNLOAD IMAGES AGAIN

    def download_images(self):
        netloc = urlparse.urlsplit(self.rootUrl).netloc.split('.')
        if netloc[-2] + netloc[-1] != self.website:
            return
        if self.rootUrl in self.urlList:
            return
        try:
            req = urllib2.Request(self.rootUrl, headers = self.hdr)
            urlContent = urllib2.urlopen(req).read()
            self.urlList.append(self.rootUrl)
        except urllib2.HTTPError as http_err:
            print http_err
            return

        self.soup = BeautifulSoup(''.join(urlContent))
        img_types = ('jpeg', 'jpg', 'gif', 'png', 'bmp')
        # find and download all images
        imgTags = self.soup.findAll('img')
        for imgTag in imgTags:
            imgUrl = imgTag['src']
            imgUrl = self.rootUrl[ : self.rootUrl.find(".com") + 4] + imgUrl if (imgUrl[ : 4] != "http") else imgUrl
            # download only the proper image files
            if imgUrl.lower().endswith(img_types):
#                imgUrl.lower().endswith('.jpg') or \
#                imgUrl.lower().endswith('.gif') or \
#                imgUrl.lower().endswith('.png') or \
#                imgUrl.lower().endswith('.bmp'):
                try:
                    req = urllib2.Request(imgUrl,headers=self.hdr)
                    imgData = urllib2.urlopen(req).read()
                    if len(imgData) >= self.minImageFileSize:
                        print "    " + imgUrl
                        fileName = basename(urlparse.urlsplit(imgUrl)[2])
                        output = open(os.path.join(self.downloadLocationPath, fileName),'wb')
                        output.write(imgData)
                        output.close()
                except Exception, e:
                    print str(e) + imgUrl

"""
# recursively download images starting from the root URL
def downloadImages(url, level): # the root URL is level 0
    # do not go to other websites
    global website
    netloc = urlparse.urlsplit(url).netloc.split('.')
    if netloc[-2] + netloc[-1] != website:
        return

    global urlList
    if url in urlList: # prevent using the same URL again
        return

    try:
        urlContent = urllib2.urlopen(url).read()
        urlList.append(url)
        print url
    except:
        return

    soup = BeautifulSoup(''.join(urlContent))
    # find and download all images
    imgTags = soup.findAll('img')
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        imgUrl = url[ : url.find(".com") + 4] + imgUrl if (imgUrl[ : 4] != "http") else imgUrl
        # download only the proper image files
        if imgUrl.lower().endswith('.jpeg') or \
            imgUrl.lower().endswith('.jpg') or \
            imgUrl.lower().endswith('.gif') or \
            imgUrl.lower().endswith('.png') or \
            imgUrl.lower().endswith('.bmp'):
            try:
                imgData = urllib2.urlopen(imgUrl).read()
                global minImageFileSize
                if len(imgData) >= minImageFileSize:
                    print "    " + imgUrl
                    fileName = basename(urlparse.urlsplit(imgUrl)[2])
                    output = open(os.path.join(downloadLocationPath, fileName),'wb')
                    output.write(imgData)
                    output.close()
            except Exception, e:
                print str(e)
                # pass
    print
    print

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:
                    linkUrl = linkTag['href']
                    downloadImages(linkUrl, level - 1)
                except Exception, e:
                    print str(e)
                    # pass
"""

def main():
    parser = argparse.ArgumentParser(description='''Downloads images from a
                                     specified URL''')
    parser.add_argument('-u', '--url', help='URL to get images from',
                        required=True)
    parser.add_argument('-r', '--rec', help='Recursion Depth (Default=0)',
                        required=False, default=0)
    parser.add_argument('-s', '--siz', help='''Minimum image size in Kb
                        (default=1)''', required=False, default=1)
    parser.add_argument('-o', '--out', help='Output directory', required=True)
    args = parser.parse_args()
    rootUrl = args.url
    maxRecursionDepth = int(args.rec)
    downloadLocationPath = args.out
    minImageFileSize = long(args.siz)

    netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
    website = netloc[-2] + netloc[-1]
    images = ImageWebsite(rootUrl, maxRecursionDepth, minImageFileSize, downloadLocationPath, website)
#    downloadImages(rootUrl, maxRecursionDepth, minImageFileSize, downloadLocationPath, website)

if __name__ == '__main__':
    main()
'''
rootUrl = cla[1]
maxRecursionDepth = int(cla[2])
downloadLocationPath = cla[3] # absolute path
if not os.path.isdir(downloadLocationPath):
    print downloadLocationPath + " is not an existing directory!"
    os._exit(2)

minImageFileSize = long(cla[4]) # in bytes
netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
website = netloc[-2] + netloc[-1]
downloadImages(rootUrl, maxRecursionDepth)
'''
