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

def printCallLog(skypeDB):
  conn = sqlite3.connect(skypeDB)
  c = conn.cursor()
  c.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM calls, "+\
            "conversations WHERE calls.conv_dbid = conversations.id;")
  print '\n[!] Calls Found: '
  for row in c:
    print '  [x] Time: %s  -> Partner: %s' %(str(row[0]), str(row[1]))

def printMessages(skypeDB):
  conn = sqlite3.connect(skypeDB)
  c = conn.cursor()
  c.execute("SELECT datetime(timestamp, 'unixepoch'), dialog_partner, author, "+\
            "body_xml FROM messages;")
  print '\n[:] Messages Found: '
  for row in c:
    try:
      if 'partlist' not in str(row[3]):
        if str(row[1]) != str(row[2]):
	  msgDirection = 'To %s :' %(str(row[1]))
	else:
	  msgDirection = 'From %s :' %(str(row[2]))
	print 'Time: %s : %s  -> %s' %(str(row[0]), msgDirection, row[3])
    except:
      pass


def main():
  skypeDB = 'main.db'
  printProfile(skypeDB)
  printContacts(skypeDB)
  printCallLog(skypeDB)
  printMessages(skypeDB)

if __name__ == '__main__':
  main()
