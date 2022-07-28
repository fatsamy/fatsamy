from utils.ex_class import exerciseload,get_last_id_new
from utils.sql_quere import max_volume
from utils.methods import ShowLastSets,get_last_id



db_path = "Diary_dbcopy.sqlite3"

lst_all = exerciseload(db_path) 
trainingsauswahl = "full_body_main_chest"
#ex_id = 30




for ex_id in range(1,9):
    last_id = get_last_id_new(ex_id,db_path)
    best_workout_id = max_volume(ex_id,db_path,lst_all)
    last_sets = ShowLastSets(last_id,ex_id,db_path)
    best_sets = ShowLastSets(best_workout_id,ex_id,db_path)
    print (f'+++++   {ex_id}  ++++')
    print (best_workout_id)
    for set in last_sets:
        print (set)

    print ()
    print (last_id)
    for setLast in best_sets:
        print (setLast)

    print ('----------')