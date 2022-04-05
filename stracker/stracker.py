from datetime import date
from flask import Blueprint, render_template, request,redirect, jsonify
import os
import json
bp = Blueprint('stracker',__name__)
from stracker.models import symptom as sy

data_model = {}
symptoms = {}
def populate():
    if os.path.exists('symptoms.json') and os.stat('symptoms.json').st_size > 0:
        with open('symptoms.json') as json_s:
            j_items = json.load(json_s)
            for k in j_items.keys():
                items = j_items[k]
                for item in items:
                    if item['Name'] not in sy.symptom.known_symptoms:
                        sy.symptom.known_symptoms.append(item['Name'])
                    symp = sy.symptom(name=item['Name'],date=item['Date'],comments=item['Notes'],mood=item['Mood'])
                    if k in data_model.keys():
                        data_model[k].append(symp)
                    else:
                        data_model[k] = [symp]
    


@bp.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        if len(data_model) == 0:
            populate()
    elif request.method == 'POST':
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
    return render_template('home.html',symptoms=data_model,known_symptoms=sy.symptom.known_symptoms)

def add_new_symptom(request):
    s_name = request.form['s_name']
    s_note = request.form['s_note']
    s_mood = request.form['s_mood']
    symp = sy.symptom(name=s_name,date=None,comments=s_note,mood=s_mood)

        #if we do not have a sypmtom for today, then add it as as key and add the symptom
    if symp.get_day() not in data_model.keys():
        data_model[symp.get_day()] = [symp]
    else:
        data_model[symp.get_day()].append(symp)
        
        #dump the data model
    with open('symptoms.json','w') as json_s:
        dump_model = {}
        for d in data_model:
            dump_model[d] = [s.get() for s in data_model[d]]
        json.dump(dump_model,json_s)



@bp.route('/new',methods=['GET','POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html',known_symptoms=sy.symptom.known_symptoms)
    else:
        if request.form['new_symptom'] != '':
            sy.symptom.add_symptom(request.form['new_symptom'])
            return render_template('new.html',known_symptoms=sy.symptom.known_symptoms)
        else:
            add_new_symptom(request)
            return render_template('home.html',symptoms=data_model,known_symptoms=sy.symptom.known_symptoms)