import sqlite3

# From Violent Python TJ O'Connor
# Python script that reads an Skype sqlite 3 DB and prints out interestin information
# The DB file must be in the current directory and be named 'main.db'

def printProfile(skypeDB):
  # Connects to the main.db file, runs a query and prints the formatted output
  conn = sqlite3.connect(skypeDB)
  c = conn.cursor()
  c.execute("SELECT fullname, skypename, city, country, " +\
            "datetime(profile_timestamp, 'unixepoch') FROM Accounts;")
  for row in c:
    print '[*] Account Found:'
    print '    [+] User: %s' %(row[0])
    print '    [+] Skype Username: %s' %(row[1])
    print '    [+] Location: %s, %s' %(row[2], row[3])
    print '    [+] profile Date: %s' %(row[4])

def printContacts(skypeDB):
  # reads the main.db file, runs a query and calls a function that verifies that
  # what's going to be printed is actually holding a value before being printed
  conn = sqlite3.connect(skypeDB)
  c = conn.cursor()
  c.execute("SELECT displayname, skypename, city, country, phone_mobile, "+\
            "birthday FROM contacts;")
  for row in c:
    print '\n  [*] Contact Found: '
    cond_print('   [-] User: ', row[0])
    cond_print('   [-] Skype Username: ', row[1])
    cond_print('   [-] Location (1): ', row[2])
    cond_print('   [-] Location (2): ', row[3])
    cond_print('   [-] Mobile Number: ', row[4])
    cond_print('   [-] Birthday: ', row[5])
    
def cond_print(text, var):
  # This function recives a text and a variable. If the variable has a value
  # meaning is different that None. It will print the text and the value
  # including int and str
  if var :
    if (isinstance(var, int)):
      print text + str(var)
    else:
      print text + var

def main():
  skypeDB = 'main.db'
  printProfile(skypeDB)
  printContacts(skypeDB)

if __name__ == '__main__':
  main()
