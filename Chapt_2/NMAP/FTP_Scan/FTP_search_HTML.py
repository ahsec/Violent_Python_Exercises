#!/usr/bin/python
import ftplib

def returnDefault(ftp):
  try:
    dirList = ftp.nlst()
  except:
    dirList = []
    print '[-] could not list directory contents'
    print '[-] Skipping to Next Target'
    return 
  retList = []
  for filename in dirList:
    fn = filename.lower()
    if ('.php' in fn) or ('.htm' in fn) or ('.asp' in fn):
      print '[+] Found default Page: %s' %(filename)
      retList.append(filename)
  return retList


host = '192.168.1.2'
userName = 'angelus'
passwd = '17/CoPmC07'
ftp = ftplib.FTP(host)
ftp.login(userName, passwd)
returnDefault(ftp)

