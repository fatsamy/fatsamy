# class decorator -- @dataclass
# mittem im Umschreiben auf volle Daten in Klassen.
# middle ist fertig und läuft!!!!
# die anderen sind noch im alten Format kopiert. Könnten funktionieren
# sollten aber umgeschrieben werden :)
import os,zipfile
from utils.sql_quere import max_volume


from utils.ex_class import * #exerciseload,find_exercise_id,take_set_list
from utils.methods import *
from utils.work_class import *
from utils.backupzip import zip

db_path = 'Irina_Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
#db_path = 'Diary_dbcopy.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
ex_db_path = 'Diary_db.sqlite3' # DB für Übungen
trainings_auswahl = 'full_body_main_chest'
# ************ Datensicherung ************* 

date,start_time,lt_start = get_date_and_time() 


# ********** TRAININGSAUSWAHL **********

print ('\n =====>  Daten wurden aus {} geladen. <======'.format(db_path))
lst_all = exerciseload(ex_db_path)
print ('\nDie letzten 5 Trainings waren.....')
_ = input()
print ('_____ Hier sind die möglichen Trainingseinheiten ____')
lst_exercise = (1,3,2,5,2)

for i in lst_exercise:
    print (Name der Übung)

question = input('Möchtest du dieses Training starten? j/n')
 
# ****** ERSTELLUNG DER HAUPTDATEN *******

# ******* Erstellung der einzelnen Sätze ******

CurrentWorkout = Workout(type=trainings_auswahl,
            current_date=date, 
            time_start=start_time,
            )
CurrentWorkout.get_current_id(db_path)
CurrentWorkout.take_temp_fasted()
CurrentWorkout.start_warmup()


for one_exercise in lst_exercise: #Name und Beschreibung anzeigen
    best_workout_id = 0
    print('')
    cur_ex = (lst_all[one_exercise-1])
    print (cur_ex)
    print('')
    print('****** Beim letztem Training: *****')
    last_sets = (ShowLastSets(last_id,one_exercise,db_path))
    for one in last_sets:
        #print (one)
        show_set(one)
    print('****** Beim BESTEM Training *******')
    best_workout_id = max_volume(one_exercise,db_path)
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



