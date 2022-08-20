#from utils.methods import show_endurance_low_middle
from re import L
from utils.work_class import EnduranceWorkout,show_endurance_low_middle
from utils.methods import dbopen
id = 117
path = 'Diary_dbcopy.sqlite3'

show_endurance_low_middle(id,path)

#with dbopen(path) as c:
#        c.execute('''SELECT * FROM sets
#                WHERE workout_id = ?
#                ''',(id,))
#        table_sets = c.fetchall()
#        c.execute('''SELECT * FROM workout_diary
#                WHERE workout_id = ?
#                ''',(id,))
#        table_workout = c.fetchall()
#table_workout = table_workout[0]
#table_sets = table_sets[0]
#print (table_workout)
#print (table_sets)
#LastWorkout = EnduranceWorkout(
#                type=table_workout[1],
#                current_date=table_workout[2],
#                time_start=table_workout[3],
#                )
#LastWorkout.id=table_workout[0]
#LastWorkout.duration=table_workout[4]
#LastWorkout.temperatur=table_workout[5]
#LastWorkout.fasted_since=table_workout[6]
#LastWorkout.avarage_puls=table_workout[7]
#LastWorkout.warmup_mins=table_workout[8]
#LastWorkout.cooldown_mins=table_workout[9]
#LastWorkout.endumins=table_sets[5]
#LastWorkout.cals=table_sets[8]
#LastWorkout.distance=table_sets[9]
#LastWorkout.workoutmemo=table_sets[10]
#print (LastWorkout)
