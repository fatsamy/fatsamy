'''Programm shows you your last workouts. You can choose
    what workout you want for today.
    After your imput for "temperatur" and "fasted since"
    the programm shows you your last sets of this workout
    and you can input your current sets with weights and
    repetitions. When all exercises are done, you can input 
    your "puls" and the date will be saved.
'''
# class decorator -- @dataclass

import os

from utils.backupzip import zip
from utils.ex_class import *  # exerciseload,find_exercise_id,take_set_list
from utils.methods import *
from utils.sql_quere import choose_db, max_volume
from utils.work_class import *

EX_DB_PATH = 'Diary_db.sqlite3'
db_path = choose_db()
#db_path = 'Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
#db_path = 'Diary_dbcopy.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN

# ************ Datensicherung *************

date,start_time,lt_start = get_date_and_time()
lst = os.listdir() # Backup von allen Dateien im Ordner. Keine Unterordner
for i in lst:
    if '.' in i:
        zip(i,'DB_Backup2/{}.zip'.format(date))

#os.chdir('DB_Backup2')
#print (os.listdir())
#os.chdir('../')

# ********** TRAININGSAUSWAHL **********

print ('\n =====>  Daten wurden aus {} geladen. <======'.format(db_path))
lst_all = exerciseload(EX_DB_PATH)
print ('\nDie letzten 5 Trainings waren.....')
_ = input()
last_five(db_path) #Anzeigen der letzten 5 Trainingseinheiten
_ = input()
print ('_____ Hier sind die möglichen Trainingseinheiten ____')
workout_pool = all_possible_workouts(EX_DB_PATH)
question = 'n'
while question == 'n':
    trainings_auswahl = ''
    while trainings_auswahl not in workout_pool:
        trainings_auswahl =  input('\nWelches Training steht heute an??')

    last_id = get_last_id(trainings_auswahl,db_path)
    lst_exercise = get_exercise(last_id,db_path)

    print (f'\n_____ Hier die Daten vom letzten Training : {trainings_auswahl}')
    if 'bike' not in trainings_auswahl:
        for i in lst_exercise:
            print (lst_all[i-1])

    else:
        if 'high' in trainings_auswahl:
            show_endurance_high(last_id,db_path)
        else:
            show_endurance_low_middle(last_id,db_path)
    question = input('Möchtest du dieses Training starten? j/n')

# ****** ERSTELLUNG DER HAUPTDATEN *******

# ******* Erstellung der einzelnen Sätze ******
if 'high' in trainings_auswahl:
    #current_id = get_current_id(db_path)
    CurrentWorkout = Workout(type=trainings_auswahl,
                current_date=date,
                time_start=start_time,
                )
    CurrentWorkout.get_current_id(db_path)
    CurrentWorkout.take_temp_fasted()
    CurrentWorkout.start_warmup()
    #save_workout_strength(CurrentWorkout.type,
    #               CurrentWorkout.current_date,
    #               CurrentWorkout.time_start,
    #               CurrentWorkout.temperatur,
    #               CurrentWorkout.fasted_since,
    #               CurrentWorkout.warmup_mins,
    #               db_path
    #               )
    exercise_id = find_exercise_id(trainings_auswahl,lst_all)
    print('Training starten....! Restlichen Eingaben nach dem Ausdauertraining')
    puls = take_set_endurance_high(exercise_id,CurrentWorkout.id, db_path)
    CurrentWorkout.take_puls()
    print ('')
    CurrentWorkout.start_cooldown()
    lt_finish = time.localtime()
    CurrentWorkout.take_timespan(lt_start,lt_finish)
    with dbopen(db_path) as c:
        c.execute('''UPDATE workout_diary
                    SET duration = ?, cooldown_mins = ?
                    WHERE workout_id = ?
                    ''',(CurrentWorkout.duration,CurrentWorkout.cooldown_mins,CurrentWorkout.id))


elif 'middle' in trainings_auswahl or 'low' in trainings_auswahl:
    #current_id = get_current_id(db_path)
    CurrentWorkout = EnduranceWorkout(type=trainings_auswahl,
                current_date=date,
                time_start=start_time,
                )
    CurrentWorkout.get_current_id(db_path)
    CurrentWorkout.take_temp_fasted()
    CurrentWorkout.start_warmup()
    print('Training starten....! Restlichen Eingaben nach dem Ausdauertraining')
    CurrentWorkout.take_mins()
    CurrentWorkout.take_puls()
    CurrentWorkout.take_cals()
    CurrentWorkout.take_distance()
    CurrentWorkout.take_memo()
    print ('')
    CurrentWorkout.start_cooldown()
    lt_finish = time.localtime()
    CurrentWorkout.take_timespan(lt_start,lt_finish)
    print (CurrentWorkout)
    # Evtl in eine Datei speichern??
    exercise_id = find_exercise_id(trainings_auswahl,lst_all)

    save_workout_endurance_low(CurrentWorkout.id,
                   CurrentWorkout.type,
                   CurrentWorkout.current_date,
                   CurrentWorkout.time_start,
                   CurrentWorkout.temperatur,
                   CurrentWorkout.fasted_since,
                   CurrentWorkout.warmup_mins,
                   CurrentWorkout.cooldown_mins,
                   CurrentWorkout.duration,
                   CurrentWorkout.endumins,
                   CurrentWorkout.avarage_puls,
                   CurrentWorkout.cals,
                   CurrentWorkout.distance,
                   CurrentWorkout.workoutmemo,
                   exercise_id,
                   db_path
                   )

else:
    CurrentWorkout = Workout(type=trainings_auswahl,
                current_date=date,
                time_start=start_time,
                )
    CurrentWorkout.get_current_id(db_path)
    CurrentWorkout.take_temp_fasted()
    CurrentWorkout.start_warmup()


    for one_exercise in lst_exercise:
        best_workout_id = 0
        print('')
        cur_ex = (lst_all[one_exercise-1])
        print (cur_ex)
        print('')
        print('****** Beim LETZTEM Training: *****')
        last_sets = (ShowLastSets(last_id,one_exercise,db_path))
        for one in last_sets:
            #print (one)
            show_set(one)
        print('\n****** Beim BESTEM Training *******')
        best_workout_id = max_volume(one_exercise,db_path,lst_all)
        best_sets = (ShowLastSets(best_workout_id,one_exercise,db_path))
        for best_set in best_sets:
            #print (best_set)
            show_set(best_set)
        #heaviest_set = show_heaviest_set(one_exercise,db_path)
        #print (heaviest_set)
        cur_ex.take_set_lst()

    print('\n\n---->>> ALLE SETS ERLEDIGT <<<----')

    CurrentWorkout.take_puls()

    print ('')
    CurrentWorkout.start_cooldown()
    lt_finish = time.localtime()
    CurrentWorkout.take_timespan(lt_start,lt_finish)

    save_workout_strength(CurrentWorkout.id,
                   CurrentWorkout.type,
                   CurrentWorkout.current_date,
                   CurrentWorkout.time_start,
                   CurrentWorkout.duration,
                   CurrentWorkout.temperatur,
                   CurrentWorkout.fasted_since,
                   CurrentWorkout.avarage_puls,
                   CurrentWorkout.warmup_mins,
                   CurrentWorkout.cooldown_mins,
                   db_path,
                   lst_exercise,
                   lst_all
                   )


print ('                      **** TRAINING BEENDET ****')
print ('                      **** DATEN GESPEICHERT ***')
