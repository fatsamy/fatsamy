import sqlite3
from utils.methods import dbopen

db_irina = 'Irina_Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
db_eugen = 'Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
db_test = 'Diary_dbcopy.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN

def choose_db():
    possible_options = ['i','e','t']
    selected = ''
    while selected not in possible_options:
        selected = input('Welche Datenbank laden? Eugen(e), Irina(i) oder Test(t) ===> ')
    if selected == 'i':
        return db_irina
    elif selected == 'e':
        return db_eugen
    else:
        return db_test





def max_volume(exercise = int, path = str): # sql quere in for-schleife
    max_volume = 0
    best_workout = 0
    with dbopen(path) as c:
        for work_id in c.execute(''' SELECT DISTINCT workout_id
                            FROM sets
                            WHERE exercise_id = ?
                            ''',(exercise,)):
            #print (work_id[0])
            sum = 0
            with dbopen(path) as cu:
                for set in cu.execute('''SELECT weight_kg,repetition
                        FROM sets
                        WHERE workout_id = ? AND exercise_id = ?
                        ''',(work_id[0],exercise)):
                    #print (set)
                    if set[0] == 0:
                        sum += 80*set[1]
                    else:
                        sum += set[0]*set[1]
            #print (sum)
            if sum > max_volume:
                max_volume = sum
                best_workout = work_id[0]
    return best_workout
               
    #print (max_volume, best_workout)



