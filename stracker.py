from datetime import date
from flask import Blueprint, render_template, request,redirect, jsonify
import os
import json
from flask_sqlalchemy import SQLAlchemy as sqlalchemy
from datetime import datetime
from stracker.models import symptom as sy
from stracker.models import datamodel as dm

bp = Blueprint('stracker',__name__)


data_model = dm.datamodel()
symptoms = {}
   
def populate():
     if os.path.exists('stracker/symptoms.json') and os.stat('symptoms.json').st_size > 0:
        with open('symptoms.json') as json_s:
            j_items = json.load(json_s)
            for k in j_items.keys():
                items = j_items[k]
                for item in items:
                    #if we haven't seen this symptom before, add it to the known symptoms.
                    if item['Name'] not in sy.symptom.known_symptoms:
                        sy.symptom.known_symptoms.append(item['Name'])
                    #create an instance of a symptom
                    symp = sy.symptom(name=item['Name'],date=item['Date'],comments=item['Notes'],mood=item['Mood'])

                    #look in the data model for the key, which is the day.
                    if k in data_model.keys():
                        data_model[k]['symptoms'].append(symp)
                        #data_model[k].append(symp)
                    else:
                        data_model[k] = {}
                        if 'symptoms' in data_model[k]:
                            data_model[k]['symptoms'] = [symp]
                        else:
                            data_model[k]['symptoms'] = [symp]
    

@bp.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if 'filter_data' in request.form.keys():
            if request.form['filter_data'] != "":
                new_col = { key:value for (key,value) in data_model.items() if key == request.form['filter_data']}
                return render_template('home.html',symptoms=new_col,known_symptoms=sy.symptom.known_symptoms)
        elif 'filter_symptomname' in request.form.keys():
            new_col = {}
            for (key,value) in data_model.items():
                for val in value:
                    if val.name == request.form['filter_symptomname']:
                        if key not in new_col.keys():
                            new_col[key] = [val]
                        else:
                            new_col[key].append(val)
                print(key)
            #new_col = { key:value for (key,value) in data_model.items() if value['Name'] == request.form['filter_symptomname']}
            return render_template('home.html',symptoms=new_col,known_symptoms=sy.symptom.known_symptoms)

        add_new_symptom(request)
    return render_template('home.html',dm=data_model)

def add_new_symptom(request):
    s_name = request.form['s_name']
    s_note = request.form['s_note']
    s_mood = request.form['s_mood']

    data_model.add_symptom(s_name=s_name,s_date=None,s_note=s_note,s_mood=s_mood)

    data_model.save()
    # with open('stracker/symptoms.json','w') as json_s:
    #     dump_model = {}
    #     for d in data_model:
    #         dump_model[d] = [s.get() for s in data_model[d]]
    #     json.dump(dump_model,json_s)



@bp.route('/new',methods=['GET','POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html',dm=data_model)
    else:
        if request.form['new_symptom'] != '':
            data_model.add_known_symptom(request.form['new_symptom'])
            return render_template('new.html',dm=data_model)
        else:
            add_new_symptom(request)
            return render_template('home.html',dm=data_model)