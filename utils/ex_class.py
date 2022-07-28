# dataclass für das ganze Workout nutzen. Alles in der Class definieren und ausfüllen lassen
# dann kann man ganz einfach alles anzeigen lassen vor dem speichern. 
# auch das abfragen könnte einfacher sein. Eine seperate Class mit sql abfragen.


from dataclasses import dataclass
from types import ClassMethodDescriptorType
from utils.methods import dbopen,i_float
from utils.decorators import timer

@dataclass(frozen=False)
class Exercise:
    id: int
    name: str
    description: str
    compound_movement: str
    target:str
    bodyweight_ex:str

    def __str__(self):
        return 'ID_{:2} === {:25} === {}'.format(self.id,self.name,self.description)
    
    @timer
    def take_set_lst(self):
        lst = []
        question_sets = 'n'
        while question_sets != 'next': 
            kg = -1
            repetition = -1
            while kg < 0 or kg > 200:
                kg = i_float('\n__Kilogramm ________:')
            while repetition <= 0 or repetition > 60:
                repetition = i_float('__Wiederholungen ___:')
            memo = ''
            question_sets =  input ('Noch ein Satz?   J/next   ') # Nach 'next' kann ein Hinweis eingefügt werden
            if question_sets == 'next':
                memo = input('**** Hinweis hinzufügen? ****')
            tlp = (kg,repetition,memo)
            lst.append(tlp)
            self.set_lst = lst
    # Sätze aufnehmen und speichern 

    def print_sets(self):
        for i in self.set_lst:
            print('{:3}Kg für {:2} Wiederholungen     Hinweis ----> {}'.format(i[0],i[1],i[2]))


def exerciseload(path):
    lst_all = []
    with dbopen(path) as c:
        c.execute('''SELECT * FROM exercise''')
        tlp = c.fetchall()
    for i in tlp:
        e = Exercise(id=i[0],name=i[1],description=i[2],compound_movement=i[3],target=i[4],bodyweight_ex=i[5])
        lst_all.append(e)
    return lst_all
    
def find_exercise(id: int, lst_all: list):
    for ex in lst_all:
        if ex.id == id:
            return ex
    raise Exception (f'Exercise with this ID {id} not found')


def find_exercise_id(name: str, lst_all: list):
    for ex in lst_all:
        if ex.name == name:
            return ex.id
    raise Exception (f'Exercise with name {name} not found')

def is_bodyweight_ex(id: int, lst_all: list):
    for ex in lst_all:
        if ex.id == id:
            return ex.bodyweight_ex
    raise Exception (f'Exercise with ID {id} not found')

def get_last_id_new(ex_id,path):
    with dbopen(path) as c:
        c.execute('''SELECT workout_id
                   FROM sets
                   WHERE exercise_id = ?
                   ORDER BY workout_id DESC
                   ''',(ex_id,)) # letzte workout_id auslesen
        last_id_tulpe = c.fetchone()
    return last_id_tulpe[0]

if __name__== '__main__':
    #db_path = 'Diary_db.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN
    db_path = 'Diary_dbcopy.sqlite3' ### ----->>> HIER DATENBANKPFAD EINGEBEN

    lst_all = exerciseload(db_path)
    #or i in lst_all:
    #   print (i)
    #xercise_name = find_exercise(39,lst_all)
    #rint (exercise_name)
    #xercise_id = find_exercise_id('racingbike_middle',lst_all)
    #print (exercise_id)#
    print (is_bodyweight_ex(2,lst_all))
    
    #    ex_1 = Exercise(id='1',name='BenchPress',description='Flachbank mit Olympiastange',compound_movement='yes',target='chest')
