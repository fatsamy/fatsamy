import os,zipfile
from utils.sql_quere import max_volume, choose_db


from utils.ex_class import * #exerciseload,find_exercise_id,take_set_list
from utils.methods import *
from utils.work_class import *
from utils.backupzip import zip

ex_db_path = 'Diary_db.sqlite3' # DB für Übungen
db_path = choose_db()

#lst_exercise = (45,31,40,16,30,5) # --------Uebungen Wählen ------
lst_exercise = (46,30,14,32,20,33) # --------Uebungen Wählen ------
#lst_exercise = (13,47,3,26,4,27) # --------Uebungen Wählen ------
current_id = 1

date,start_time,lt_start = get_date_and_time() 

last_id = 0
# ********** TRAININGSAUSWAHL **********

print ('\n =====>  Daten wurden aus {} geladen. <======'.format(db_path))
lst_all = exerciseload(ex_db_path)

print ('_____ Hier sind die möglichen Trainingseinheiten ____')
workout_pool = all_possible_workouts(ex_db_path)
question = 'n'
while question == 'n':   
    trainings_auswahl = ''  
    while trainings_auswahl not in workout_pool:
        trainings_auswahl =  input('\nWelches Training steht heute an??')
    for i in lst_exercise:
        print (lst_all[i-1])
    question = input('Möchtest du dieses Training starten? j/n')

    
 
# ****** ERSTELLUNG DER HAUPTDATEN *******

# ******* Erstellung der einzelnen Sätze ******

CurrentWorkout = Workout(type=trainings_auswahl,
            current_date=date, 
            time_start=start_time,
            )
#CurrentWorkout.get_current_id(db_path)
CurrentWorkout.id = current_id
CurrentWorkout.take_temp_fasted()
CurrentWorkout.start_warmup()


for one_exercise in lst_exercise: #Name und Beschreibung anzeigen
    print('')
    cur_ex = (lst_all[one_exercise-1])
    print (cur_ex)
    print('')
    print('****** Beim letztem Training: *****')
    last_sets = (ShowLastSets(last_id,one_exercise,db_path))
    for one in last_sets:
        #print (one)
        show_set(one)
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



