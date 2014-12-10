import sqlite3

# More violence with the Python
# This script will read and print interesting information obtained from
# Firefox's sqlite databases

def printDownloads(downloadDB):
  # Print information about the downloads made by a user. DB file: downloads.sqlite
  conn = sqlite3.connect(downloadDB)
  c = conn.cursor()
  c.execute("SELECT name, source, datetime(endTime/1000000, 'unixepoch') "+\
            "FROM moz_downloads;")
  print '\n Files Downloaded: '
  for row in c: 
    print '[+] File: %s - From source: %s -> at: %s' %(str(row[0]), str(row[1]), str(row[2]))

def main():
  downloadDB = 'downloads.sqlite'
  printDownloads(downloadDB)

if __name__ == '__main__':
  main()
