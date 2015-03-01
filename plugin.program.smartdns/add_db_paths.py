import csv, os, xbmc, subprocess


try:
    from sqlite3 import dbapi2 as sqlite
    print "Loading sqlite3 as DB engine"
except:
    from pysqlite2 import dbapi2 as sqlite
    print "Loading pysqlite2 as DB engine"

def run():
    p = subprocess.Popen(["systemctl", "stop","xbmc"], stdout=subprocess.PIPE)

    DB = os.path.join(xbmc.translatePath("special://database"), 'MyVideos78.db')
    db = sqlite.connect(DB)

    cur = db.cursor()

    csvpath = xbmc.translatePath(os.path.join('special://home','addons','plugin.program.smartdns','resources','path.csv'))

    with open(csvpath,'rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['strPath'], i['strContent'], i['strHash'], i['scanRecursive'], i['useFolderNames'], i['strSettings'], i['noUpdate'], i['exclude'], i['dateAdded']) for i in dr]

    cur.executemany("INSERT INTO path (strPath, strContent, strHash, scanRecursive, useFolderNames, strSettings, noUpdate, exclude, dateAdded) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    db.commit()
    db.close()
    p = subprocess.Popen(["systemctl", "start","xbmc"], stdout=subprocess.PIPE)

