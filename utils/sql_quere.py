import sqlite3
from utils.diarypack import dbopen


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
                    sum += set[0]*set[1]
            #print (sum)
            if sum > max_volume:
                max_volume = sum
                best_workout = work_id[0]
    return best_workout
               
    #print (max_volume, best_workout)



