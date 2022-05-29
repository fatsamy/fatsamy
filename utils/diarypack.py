import sqlite3,time



class dbopen(object):
    """
    Simple CM for sqlite3 databases. Commits everything at exit.
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()



def last_five(path):
    with dbopen(path) as c:
        c.execute('''SELECT workout_type
                    FROM workout_diary
                    ORDER BY workout_id DESC''')
        last_f = c.fetchmany(5)
    for i in last_f:
        print(f'=== {i[0]:18} ===')
    print('\n')
    # zeigt die letzten 5 Trainings an


def all_possible_workouts(path):
    with dbopen(path) as c:
        c.execute('''SELECT workout_type
                   FROM w_type
                   ''')
        all_w = c.fetchall()
    all_w2 = []
    for i in all_w: 
        all_w2 += i
    for i in all_w2:
        print(f'----- {i:20} -----')
    return all_w2
    # zeigt alle möglichen Trainings an

def fetchone_to_str(whatyouget):
        str = ''
        ints = '0123456789'
        for w in whatyouget:
            if w in ints:
                str += w
        return str
        # übergibt ein sqlite 3-fetch in einen str

def get_date_and_time():
    lt_start = time.localtime()
    date = ('{}-{:02}-{:02}'.format(lt_start[0],lt_start[1],lt_start[2]))
    start_time = ('{:02}:{:02}'.format(lt_start[3],lt_start[4]))
    return date,start_time,lt_start

def WorkoutMainData(trainings_auswahl,date,start_time,path):
    global current_id
    temp = 999
    while temp < -10 or temp > 45:
        temp = i_float('Temperatur___:')
    fasted = 999
    while fasted < 0 or fasted > 100:
        fasted = i_float('Letzte Mahlzeit vor wievielen Stunden?___:')
    print ('\n** WARMUP gestarte **')
    lt_warmup_start = time.localtime()
    input ('** WARMUP beendet ?? **')    
    lt_warmup_finish = time.localtime()
    warmup = duration_time(lt_warmup_start,lt_warmup_finish)
    with dbopen(path) as c:
        c.execute('''INSERT INTO workout_diary 
                   (workout_id,workout_type,workout_date,workout_time_start,temperature,fasted_since,warmup_mins) 
                   VALUES (NULL,?,?,?,?,?,?)
                   ''',(trainings_auswahl,date,start_time,temp,fasted,warmup))
        c.execute('''SELECT workout_id 
                   FROM workout_diary 
                   ORDER BY workout_id DESC''') # aktuelle workout_id auslesen
        aktuelle_id_tuple = c.fetchone() # aktuelle ID auselesen ist noch nicht getestet
    current_id = 0
    for i in range(0,500): 
        if i in aktuelle_id_tuple:
            current_id = i
    #print (current_id, 'ist die aktuelle ID')
    return current_id
#
def show_identical_workout_strenght(trainings_auswahl,path): 
    global exercise_names
    global last_id
    exercise_names = []
    with dbopen(path) as c:
        c.execute('''SELECT workout_id
                   FROM workout_diary 
                   WHERE workout_type = ?
                   ORDER BY workout_id DESC
                   ''',(trainings_auswahl,)) # letzte workout_id auslesen
        last_id_tulpe = c.fetchone()
    last_id = last_id_tulpe[0]
    with dbopen(path) as c:
        c.execute('''SELECT DISTINCT exercise_id
                From sets
                WHERE workout_id = ? 
                ''',(last_id,)) 
        read_exercise_id = c.fetchall()
    numbers = ()
    for i in range (0,len(read_exercise_id)):
        numbers += read_exercise_id[i]
    
    with dbopen(path) as c:
        for e in numbers:
            c.execute('''SELECT exercise_name  
                       FROM exercise 
                       WHERE exercise_id = ? 
                       ''',(str(e),))
            exercise_name = c.fetchone()
            exercise_names.append(exercise_name[0])
        
            c.execute(''' SELECT weight_kg,repetition,memo
                       From sets
                       WHERE exercise_id = ? AND workout_id = ?
                       ''',(str(e),last_id))
            exercise_sets = c.fetchall()
            print(exercise_name, exercise_sets)
    return exercise_names, last_id
        #print (exercise_name, + '{}KG für {} Wiederholungen'.format(exercise_sets[0],exercise_sets[1]))
        # Sätze und Wiederholungen vom letztem gleichem Training

def ShowLastSets(id,exercise,path):
    with dbopen(path) as c:
        c.execute('''SELECT weight_kg,repetition
                    FROM sets
                    WHERE workout_id = ? and exercise_id = ?
                    ''',(id,exercise))
        a = c.fetchall()
    return a



def fetch_workout_endurance(trainings_auswahl,path):
    with dbopen(path) as c: 
        c.execute('''SELECT workout_id
                   FROM workout_diary 
                   WHERE workout_type = ?
                   ORDER BY workout_id DESC
                   ''',(trainings_auswahl,)) # letzte workout_id auslesen
        last_id_tulpe = c.fetchone()
    #print (last_id_tulpe)
    last_id_endurance = 0
    for i in range(0,1000):
        if i in last_id_tulpe:
            last_id_endurance = i
    return last_id_endurance
    # letztes Ausdauertraining laden


def show_endurance_low_middle(id,path):
        # ----------- PULS-----------#
    with dbopen(path) as c:
        c.execute('''SELECT puls
                From workout_diary
                WHERE workout_id = ? 
                ''',(id,))
        puls = c.fetchone()
        # ----------time_in_mins ----------#
        c.execute(''' SELECT time_in_mins
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        time_in_mins = c.fetchone()
        # ---------- calories -------------#
        c.execute(''' SELECT calories
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        calories = c.fetchone()
    print ('__{}_mins mit einem Druchschnittpuls von __{}_S/mins'.format(time_in_mins[0],puls[0]))
    print ('Das bei___ {}_Calorien___ Leistung'.format(calories[0]))
    # letztes Ausdauertraining anzeigen das "low" oder "middle" war


def show_endurance_high(id,path):
        # ----------- PULS-----------#
    with dbopen(path) as c:
        c.execute('''SELECT puls
                From workout_diary
                WHERE workout_id = ? 
                ''',(id,))
        puls = c.fetchone()           
        # ----------time_on ----------#
        c.execute(''' SELECT time_on_sec
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        time_on = c.fetchone()
        # ----------time_off ----------#
        c.execute(''' SELECT time_off_sec
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        time_off = c.fetchone()
    #------------rounds------------#
        c.execute(''' SELECT time_in_mins
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        time = c.fetchone()
#------------ calories ----------#
        c.execute(''' SELECT calories
                FROM sets
                WHERE workout_id = ?
                ''',(id,))
        calories = fetchone_to_str(str(c.fetchall()))
    time_sec = int(time[0])*60
    one_round = int(time_off[0])+int(time_on[0])
    rounds = time_sec/one_round
    print ('Intervall: {}er Puls bei {} Runden je {}sec ON und {}sec OFF'.format(puls[0],rounds,time_on[0],time_off[0]))
    print ('Das bei___ {}Cal___ Leistung'.format(calories))
    # letztes Ausdauertraining anzeigen dass "high" war

def read_exercise_id(findthat,path):
    with dbopen(path) as c:
        c.execute('''SELECT exercise_id
                    FROM exercise
                    WHERE exercise_name = ?
                    ''',(findthat,))
        id = fetchone_to_str(str(c.fetchone()))
    return id 
    #findet die exercise_id von einer Übung

def describe(exercise_,path):
    with dbopen(path) as c:
        c.execute('''SELECT exercise_description
                   FROM exercise
                   WHERE exercise_name = ?
                   ''',(exercise_,))
        description = c.fetchone()
    return description[0]
    # Beschreibung auslesen


def take_set_endurance_high(exercise_id, path):
    timeON = input ('Interfallzeit ON  in Sekunden___:')
    timeOFF = input('Interfallzeit OFF in Sekunden___:')
    print('!!! ----Den Rest nach dem Training angeben---- !!!')
    mins = input('Zeit des gesamten Intervallprotokolls in Minuten: ___ ')
    avarage_puls = input('Durchschnittlicher Puls:___')
    cals = input('Calorien___:')
    distance = float(input('Wieviel KM:__:'))
    with dbopen(path) as c:
        c.execute('''INSERT INTO sets 
                    ('workout_id','set_id','exercise_id','time_in_mins','time_on_sec','time_off_sec','calories','distance_km')
                    VALUES (?,NULL,?,?,?,?,?,?)
                    ''',(current_id,exercise_id,mins,timeON,timeOFF,cals,distance))
        c.execute('''UPDATE workout_diary 
                   SET puls = (?)
                   WHERE workout_id = (?)
                   ''',(avarage_puls,current_id))
    # nimmmt ein Set für Ausdauertraining "high" auf

def take_set_endurance_low(exercise_id, path):
    mins = input('Zeit der Ausdauereinheit in Minuten: ___ ')
    avarage_puls = input('Durchschnittlicher Puls:___')
    cals = input('Calorien___:')
    distance = float(input('Wieviel KM?__:'))
    with dbopen(path) as c:
        c.execute('''INSERT INTO sets 
                    ('workout_id','set_id','exercise_id','time_in_mins','calories','distance_km')
                    VALUES (?,NULL,?,?,?,?)
                    ''',(current_id,exercise_id,mins,cals,distance))
        c.execute('''UPDATE workout_diary 
                   SET puls = (?)
                   WHERE workout_id = (?)
                   ''',(avarage_puls,current_id))
    # nimmt ein Set für Ausdauertraining "low" oder "middle" auf

def duration_time(start,finish):
    start_in_mins = start[3]*60 + start[4]
    finish_in_mins = finish[3]*60 + finish[4]
    duration = finish_in_mins-start_in_mins
    return duration
    # berechnet die Länge des Trainings nach Abschluss und speichert in DB
    
def i_float(question):
    while True:    
        try:
            b = float(input(question))
        except:
            print('Nur Zahlen möglich')
        else:
            return b
    
