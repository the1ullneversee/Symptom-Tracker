from stracker.models.symptom import symptom
from stracker.models.activity import activity
from datetime import datetime
import pyodbc

class datamodel():
    
    def __init__(self):
        self.day_model = {}
        #self.add_day(self.get_day_key())
        self.known_symptoms = []
        self.populate()
    
    def populate(self):
        with pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DESKTOP-UUOQ7VJ\SQLEXPRESS' , database = 'Symptom Tracker') as sql_con:
            for row in sql_con.execute("SELECT * FROM Symptoms"):
                s_date = row[2].strftime("%m/%d/%Y")
                if s_date not in self.day_model.keys():
                    self.day_model[s_date] = self.get_internal_collection_structure()
                self.add_symptom(date_key=s_date,s_name=row[1],s_date=row[2],s_note=row[3],s_mood=row[4])
                print(row)
        self.day_model[s_date]['activities'].append(activity("Drank Alcohol",completed=True,type='Food and Beverage'))
        self.day_model[s_date]['activities'].append(activity("Took Pill",completed=False,type='Medicine'))
        print(f"populated day_model with {len(self.day_model)} days")

    def day_key_current(self,key):
        return key == self.get_day_key()

    def get_day_key(self):
        now = datetime.now()
        s_now = now.strftime("%d/%m/%Y")
        return s_now

    def get_internal_collection_structure(self):
        return {'symptoms':[], 'activities': [], 'irritants':[]}

    def add_day(self,day):
        self.day_model[day] = self.get_internal_collection_structure()
    
    def add_known_symptom(self,s_name):
        if s_name not in self.known_symptoms:
            self.known_symptoms.append(s_name)

    def add_symptom(self,date_key,s_name,s_date,s_note,s_mood):
        if s_name not in self.known_symptoms:
            self.known_symptoms.append(s_name)
        
        self.day_model[date_key]['symptoms'].append(symptom(name=s_name,date=s_date,comments=s_note,mood=s_mood))

    def save(self):
         #dump the data model
        with pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DESKTOP-UUOQ7VJ\SQLEXPRESS' , database = 'Symptom Tracker') as sql_con:
            now = datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            for symptom in self.day_model[self.get_day_key()]['symptoms']:
                sql_con.execute(f"INSERT INTO Symptoms (Name,Date,Notes,Mood) VALUES('{symptom.get_name()}','{symptom.get_date_str()}','{symptom.get_comments()}','{symptom.get_mood()}')")
