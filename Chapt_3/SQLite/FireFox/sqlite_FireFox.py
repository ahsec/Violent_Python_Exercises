import sqlite3
import re

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

def printCookies(cookiesDB):
  # Print cookies stored in Firefox's database. Name and value of each delicious cookie
  try:
    conn = sqlite3.connect(cookiesDB)
    c = conn.cursor()
    c.execute("SELECT host, name, value FROM moz_cookies;")
    print '\n[!] Cookies found: '
    for row in c:
      host = str(row[0])
      name = str(row[1])
      value = str(row[2])
      print '  [:] Host: %s -> Cookie: %s -> Value: %s' %(host, name, value)
  except Exception as e:
    if 'encrypted' in str(e):
      print '\n [x] Error reading your cookies DB'
      print '   Upgrade your sqlite3 DBM'

def printHistory(placesDB):
  # Print the browsing history and if a Google search is found it is stored
  # in a list and the terms searched ripped and presented
  G_search = []
  try:
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, "+\
              "moz_historyvisits WHERE visit_count > 0 and moz_places.id == "+\
	      "moz_historyvisits.place_id;")
    print '\n[+] History found:'
    for row in c:
      url = str(row[0])
      date = str(row[1])
      print '%s - Visited: %s' %(url, date)
      if 'google' in url.lower():
        r = re.findall(r'q=.*\&',url)
	if r:
	  search = r[0].split('&')[0]
	  search = search.replace('q=', '').replace('+', ' ')
	  G_search.append('[+] %s - Searched for: %s' %(date, search))
    print '\n[#] Searches found: '
    for search in G_search:
      print search
  except Exception as e:
    if 'encrypted' in str(e):
      print '\n [x] Error reading your places DB'
      print '   Upgrade your sqlite3 DBM'
      
def main():
  downloadDB = 'downloads.sqlite'
  printDownloads(downloadDB)
  cookiesDB = 'cookies.sqlite'
  printCookies(cookiesDB)
  placesDB = 'places.sqlite'
  printHistory(placesDB)

if __name__ == '__main__':
  main()
