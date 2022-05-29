# class decorator -- @dataclass
# mittem im Umschreiben auf volle Daten in Klassen.
# middle ist fertig und läuft!!!!
# die anderen sind noch im alten Format kopiert. Könnten funktionieren
# sollten aber umgeschrieben werden :)
import os,zipfile


from utils.ex_class import * #exerciseload,find_exercise_id,take_set_list
from utils.methods import *
from utils.work_class import *
from utils.backupzip import zip

#db_path = 'Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
db_path = 'Diary_dbcopy.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN

# ************ Datensicherung ************* 

date,start_time,lt_start = get_date_and_time() 

# ********** TRAININGSAUSWAHL **********

print ('\n =====>  Daten wurden aus {} geladen. <======'.format(db_path))
lst_all = exerciseload(db_path)
print ('\nDie letzten 5 Trainings waren.....')
last_five(db_path) #Anzeigen der letzten 5 Trainingseinheiten
print ('_____ Hier sind die möglichen Trainingseinheiten ____')
workout_pool = all_possible_workouts(db_path)
question = 'n'
while question == 'n':   
    trainings_auswahl = ''  
    while trainings_auswahl not in workout_pool:
        trainings_auswahl =  'full_body_main_chest' #input('\nWelches Training steht heute an??')

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
    question = 'j' #input('Möchtest du dieses Training starten? j/n')
 
# ****** ERSTELLUNG DER HAUPTDATEN *******

# ******* Erstellung der einzelnen Sätze ******
#save_workout_strength(CurrentWorkout.type,   
#               CurrentWorkout.current_date,
#               CurrentWorkout.time_start,
#               CurrentWorkout.temperatur,
#               CurrentWorkout.fasted_since,
#               CurrentWorkout.warmup_mins,
#               db_path
#               )

#current_ex_pool = WorkoutMainData(trainings_auswahl,date,start_time,db_path) #--- Aufnahmen der Einzelnen Übungen mit Gewichten und Sätzen
#for one_exercise in lst_exercise: #Name und Beschreibung anzeigen
#    print('')
#    cur_ex = (lst_all[one_exercise-1])
#    print (cur_ex)
#    print('')
#    last_sets = (ShowLastSets(last_id,one_exercise,db_path))
#    for one in last_sets:
#        show_set(one)
#    cur_ex.take_set_lst()
#    #print (cur_ex.set_lst)
#for one_exercise in lst_exercise:
#    cur_ex2 = (lst_all[one_exercise-1])
#    cur_ex2.print_sets()
#    print ()
if 0 == 0:
    #current_id = get_current_id(db_path)
    CurrentWorkout = Workout(type=trainings_auswahl,
                current_date=date, 
                time_start=start_time,
                )
    CurrentWorkout.get_current_id(db_path)
    CurrentWorkout.take_temp_fasted()
    CurrentWorkout.start_warmup()
    
    
    #current_ex_pool = WorkoutMainData(trainings_auswahl,date,start_time,db_path) #--- Aufnahmen der Einzelnen Übungen mit Gewichten und Sätzen
    for one_exercise in lst_exercise: #Name und Beschreibung anzeigen
        print('')
        cur_ex = (lst_all[one_exercise-1])
        print (cur_ex)
        print('')
        last_sets = (ShowLastSets(last_id,one_exercise,db_path))
        for one in last_sets:
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



