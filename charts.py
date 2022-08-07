from datetime import date
from matplotlib import pyplot as plt
from utils.methods import dbopen
from utils.diagramm import single_plot,max_plot
from utils.ex_class import exerciseload, is_bodyweight_ex,find_exercise_name



def exercise_chart(exercise = int ,path = str, lst_all = list):
    workout_id_lst = []
    volume_lst = []
    bodyweight = 0
    if is_bodyweight_ex(exercise,lst_all) == 'yes':
        bodyweight = 80
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
                    sum += (set[0]+bodyweight)*set[1]
            workout_id_lst.append(work_id)
            volume_lst.append(sum)
    return workout_id_lst,volume_lst
            





if __name__ == '__main__':
    #db_path = 'Diary_db.sqlite3'
    db_path = 'Irina_Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN

    ex_db_path = 'Diary_db.sqlite3'


    lst_all = exerciseload(ex_db_path)
    
    all_for_plot = []
    for ex in lst_all:
        #if 'legs' in ex.target:
        if ex.target != 'endurance':
            all_for_plot.append(ex.id)
    #print (all_for_plot)
            
    for i in all_for_plot:
        workout_id_lst,volume_lst = exercise_chart(i,db_path,lst_all)
        max_plot('Workout_ID', 
                    workout_id_lst, 
                    'GesamtVolumen', 
                    volume_lst, 
                    find_exercise_name(i,lst_all))
        #print(i)
    
    plt.show()
