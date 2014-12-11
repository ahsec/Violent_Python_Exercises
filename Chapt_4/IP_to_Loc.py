import pygeoip

# From book ViolenPython TJ O'Connor with some changes of mine
# This script will use publicly available info from MaxMind GeoLiteCity DB
# To correlate an IP address to a physical location

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def printRecord(tgt):
  # Where the juice is produced !!
  # Gets the info from the DB file and formats the output
  rec = gi.record_by_name(tgt)
  city = rec['city']
  region = rec['metro_code']
  country = rec['country_name']
  longt = rec['longitude']
  lat = rec['latitude']
  print '[*] Target: %s GeoLocated' %(tgt)
  print ' [+] %s, %s, %s' %(city, region, country)
  print ' [+] Latitude: %s, Longitude: %s' %(longt, lat)

def main():
  gi = pygeoip
  tgt = '173.255.226.98'
  printRecord(tgt)

if __name__ == '__main__':
  main()
