import os
import sqlite3

# Violent Python.
# Function that prints the tables of all the sqlite databases found in 
# the local directory

def printTables(filename):
  try:
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute('SELECT tbl_name FROM sqlite_master WHERE '+\
              'type == "table";')
    print '\nDatabase: %s' %(filename)
    for row in c:
      print '[*] Table: %s' %(row)
    conn.close()
  except:
    pass

def main():
  dirList = os.listdir(os.getcwd())
  for filename in dirList:
    printTables(filename)

if __name__ == '__main__':
  main()
