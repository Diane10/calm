from distutils.log import debug
from time import time

# from flask import Flask, flash,render_template,request    
from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask import Flask
import pickle
import flask
from sklearn.neighbors import KNeighborsClassifier
import datetime



labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    


app = Flask(__name__)

# stress fsurvey rendering
@app.route('/stress_route')
def stress_route():
    return render_template('stress_forms.html')

# Anxiety survey
@app.route('/anxiety_route')
def anxiety_route():
    return render_template('anxiety_forms.html')

# depression
@app.route('/depression_route')
def depression_route():
    return render_template('depression_forms.html')
# home survey
# @app.route('/home')
# def home_route():
#     return render_template('home.html')

@app.route('/')
def login():
    # population=50
    # bar_labels=labels
    # bar_values=values
    # pie_labels = labels
    # pie_values = values
    # line_labels=labels
    # line_values=values
    # return render_template('stress.html',population=population,title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values,label=line_labels, value=line_values,set=zip(values, labels, colors))
    return render_template('home.html')

@app.route('/form_login',methods=['POST','GET'])
def login_page():
    
    model_parameters = []
    
    # append result in the array
    for i in range(1,15):
        model_parameters.append(int(request.form['q'+str(i)]))

    # calculate score
    score = sum(model_parameters)

    model_parameters.append(score)

    with open('depression_model.pkl' , 'rb') as f:
        loaded_model = pickle.load(f)

    # loaded_model = pickle.load(open('model.pkl', 'rb'))

    predic_stress = loaded_model.predict([model_parameters])

    ts = datetime.datetime.now()

    day = ts.day
    mn = ts.month
    yr = ts.year

    min = ts.minute
    hr = ts.hour


    timestampStr = str(day) + ' ' + str(ts.strftime("%b")) + '  '+ str(hr) + ' : ' + str(min)
    print(timestampStr)
    
    
    return render_template('stress.html', t=timestampStr, array = model_parameters, results = predic_stress)

# For anxiety
@app.route('/form_anxiety',methods=['POST','GET'])
def anxiety_page():
    
    model_parameters = []
    
    # append result in the array
    for i in range(1,15):
        model_parameters.append(int(request.form['q'+str(i)]))

    # calculate score
    score = sum(model_parameters)

    model_parameters.append(score)

    with open('anxiety_model.pkl' , 'rb') as f:
        loaded_model = pickle.load(f)

    # loaded_model = pickle.load(open('model.pkl', 'rb'))

    predic_stress = loaded_model.predict([model_parameters])
    

    
    return render_template('test.html', array = model_parameters, results = predic_stress)


def get_right_percentage(bin):
    percentage_bins = {'Normal': 20,'Mild': 40, 'Moderate':60, 'Severe':80, 'Extremely Severe': 100}
    return percentage_bins[bin]

def righ_level_color(level_percent):
    if(level_percent < 50):
        return 'w3-light-blue'
    return 'w3-red'



# Test choices_stress form
@app.route('/choices_stress',methods=['POST','GET'])
def stress_page():

    # get the array of choices from 'btn0' name 'all_choices'

    model_parameters = []
    choices_sent = request.form['choice']
    split_results = choices_sent.split(',')
    identify = request.form['identity']

    # make the array intigers
    for element in split_results:
        model_parameters.append(int(element))
    
    # append result in the array
    # for i in range(1,15):
    #     model_parameters.append(int(request.form['q'+str(i)]))

    # calculate score
    score = sum(model_parameters)

    model_parameters.append(score)

    # use the right model
    # stress
    if(identify == 'Stress'):

        with open('stress_model.pkl' , 'rb') as f:
            loaded_model = pickle.load(f)
    # Anxiety 
    if(identify == 'Anxiety'):

        with open('anxiety_model.pkl' , 'rb') as f:
            loaded_model = pickle.load(f)
    # adepression
    if(identify == 'Depression'):

        with open('depression_model.pkl' , 'rb') as f:
            loaded_model = pickle.load(f)
    

    # # loaded_model = pickle.load(open('model.pkl', 'rb'))
    

    predic_stress = loaded_model.predict([model_parameters])

    ts = datetime.datetime.now()

    day = ts.day
    mn = ts.month
    yr = ts.year

    min = ts.minute
    hr = ts.hour


    timestampStr = str(day) + ' ' + str(ts.strftime("%b")) + '  '+ str(hr) + ' : ' + str(min)
    print(timestampStr)

    

    



    
    

    
    return render_template('prediction.html',t=timestampStr, color = righ_level_color(get_right_percentage(predic_stress[0])) , results = predic_stress[0], identify=identify, level = get_right_percentage(predic_stress[0]))



if __name__ == '__main__':
    app.run(host='0.0.0.0')