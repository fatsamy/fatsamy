import time


from dataclasses import dataclass

from utils.methods import duration_time,i_float,dbopen



@dataclass    
class Workout:
    type: str
    current_date: str
    time_start: str 
    
    def __post_init__(self):
        pass

    def __str__(self):
        return '''ID{:2} {} {}\n
                Temp:{}C\n
                Fasted: {}h\n
                Time: {}\n
                Warmup: {}\n
                Cooldown: {}\n
                Puls: {}\n
                Duration: {}\n
                WorkoutMemo: {}'''.format(
            self.id,
            self.type,
            self.current_date,
            self.temperatur,
            self.fasted_since,
            self.time_start,
            self.warmup_mins,
            self.cooldown_mins,
            self.avarage_puls,
            self.duration,
            self.workoutmemo
            )
    
    def get_current_id(self,path):
        with dbopen(path) as c:
            c.execute('''SELECT workout_id 
                       FROM workout_diary 
                       ORDER BY workout_id DESC''') 
            aktuelle_id_tuple = c.fetchone() 
        self.id = aktuelle_id_tuple[0]+1
        
    # aktuelle workout_id auslesen 


    def start_warmup(self):
        print ('\n** WARMUP gestarte **')
        lt_warmup_start = time.localtime()
        input ('** WARMUP beendet ?? **')    
        lt_warmup_finish = time.localtime()
        self.warmup_mins = duration_time(lt_warmup_start,lt_warmup_finish)#

    def start_cooldown(self):   
        lt_cooldown_start = time.localtime()
        print (' *** Übungen beendet - Cooldwon gestarted.... ')
        print ('')
        input ('*** Training beenden?  / Enter***')
        lt_cooldown_finish = time.localtime()
        cooldown = duration_time(lt_cooldown_start,lt_cooldown_finish)
        self.cooldown_mins = cooldown

    def take_temp_fasted(self):
        temp = 999
        while temp < -10 or temp > 45:
            temp = i_float('Temperatur___:')
        self.temperatur = temp
        fasted = 999
        while fasted < 0 or fasted > 100:
            fasted = i_float('Letzte Mahlzeit vor wievielen Stunden?___:')
        self.fasted_since = fasted
        
    def take_puls (self):  
        p = -1
        while p <= 90 or p > 180:
            p = i_float('Durchschnittlicher Puls....')
        self.avarage_puls = p 


    def take_timespan(self,start,end):
        self.duration = duration_time(start,end)

    def take_memo(self):
        memo = input('WorkoutMemo hinzufügen?')
        self.workoutmemo = memo
@dataclass
class EnduranceWorkout(Workout):
    def __str__(self):
        return '''ID{:2} {} {}\n
                Temp:{}C\n
                Fasted: {}h\n
                Time: {}\n
                Warmup: {}\n
                Cooldown: {}\n
                Puls: {}\n
                ZeitGesamt: {}\n
                ZeitAusdauereinheit: {}\n
                Kalorien: {}\n
                Distanz: {}\n
                WorkoutMemo: {}'''.format(
            self.id,
            self.type,
            self.current_date,
            self.temperatur,
            self.fasted_since,
            self.time_start,
            self.warmup_mins,
            self.cooldown_mins,
            self.avarage_puls,
            self.duration,
            self.endumins,
            self.cals,
            self.distance,
            self.workoutmemo
            )

        

    def take_mins(self):
        mins = i_float('Zeit der Ausdauereinheit in Minuten: ___')
        self.endumins = mins
    
    def take_cals(self):
        cals = i_float('Calorien:___')
        self.cals = cals

    def take_distance(self):
        d = i_float('Wieviel Km?: ___')
        self.distance = d

    