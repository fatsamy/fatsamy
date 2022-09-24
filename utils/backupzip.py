# Programm  speichert aktuell nur Diary_db.sqlite3 in eine Zip bei Diary/DB_Backup
# wenn das öfter am Tag ausgeführt wird, wird alles in einer Zip gespeichert
# ---> DAS MUSS ABER NOCH GETESTET WERDEN
# Sollte man das noch automatisch starten lassen? 


import os, zipfile


#print(os.getcwd()) # Show current working directory



def zip(datei, zipDatei):
    if os.path.isfile(datei):
        if os.path.isfile(zipDatei):
            zip = zipfile.ZipFile(zipDatei, 'a')
        else:
            zip = zipfile.ZipFile(zipDatei, 'w')
        zip.write(datei)
        zip.close()
    else:
        print (datei, "existiert nicht.")
    
if __name__ == '__main__':
    date = 'testname'
    lst = os.listdir()
    for i in lst:
        if '.' in i:
            zip(i,'DB_Backup/{}.zip'.format(date))

    os.chdir('DB_Backup')
    print (os.listdir())