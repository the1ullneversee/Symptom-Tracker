from datetime import datetime
from time import strftime
import json



class symptom:
    known_symptoms = []
    def __init__(self,name,date,comments,mood):
        self.name = name
        if not date:
            now = datetime.now()
            self.date = now
            self.day = now.strftime("%d/%m/%Y")
            self.time = now.strftime("%H:%M:%S")
        else:
            self.date = datetime.strptime(date,"%d/%m/%Y %H:%M:%S")
            self.day = self.date.strftime("%d/%m/%Y")
            self.time = self.date.strftime("%H:%M")
        self.comments = comments
        self.mood = mood
    
    def add_symptom(symp):
        symptom.known_symptoms.append(symp)

    def get(self):
        return {"Name":self.name,"Date":self.date.strftime("%d/%m/%Y %H:%M:%S"),"Notes": self.comments,"Mood":self.mood}
    
    def get_name(self):
        return self.name
    
    def get_date(self):
        return self.date
    
    def get_day(self):
        return self.day

    def get_time(self):
        return self.time
    
    def get_comments(self):
        return self.comments

    def get_mood(self):
        return self.mood

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,indent=4)
    