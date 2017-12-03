from flask import Flask, render_template, request, redirect, session, json, jsonify, url_for
import requests


app = Flask(__name__)


tribos_dict = {'caetes': 0, 'caiapos': 0, 'caingangue': 0, 'guajajaras': 0, 'guaranis': 0, 'ianomamis': 0, 'macuxi': 0, 'marubos': 0, 'pataxos': 0, 'potiguaras': 0, 'tapuias': 0, 'terenas': 0, 'ticunas': 0, 'xavantes': 0}

@app.route('/')
def quiz():

    tribos_dict = dict.fromkeys(tribos_dict, 0)

    return render_template('quiz.html')

@app.route('/validateQuiz', methods = ["POST"])
def validateQuiz():
    #TODO

    historia = int(request.form['historia'])
    lingua = int(request.form['lingua'])
    cultura = int(request.form['cultura'])
    religiao = int(request.form['religiao'])
    locpop = int(request.form['locpop'])
    dieta = int(request.form['dieta'])


    if lingua == 1:
        tribos_dict['caiapos'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['xavantes'] +=1
    elif lingua == 2:
        tribos_dict['caetes'] +=1
        tribos_dict['guajajara'] +=1
        tribos_dict['guarani'] +=1
        tribos_dict['tapuias'] +=1
    elif lingua == 3:
        tribos_dict['pataxos'] +=1
    elif lingua == 4:
        tribos_dict['terena'] +=1
    elif lingua == 5:
        tribos_dict['ticunas'] +=1
    elif lingua == 6:
        tribos_dict['marubos'] +=1

    







@app.route('/youInsper2')
def hello2():
    result = firebase.get('/videos', None)

    del videos[:]
    del sum_ratings[:]
    del n_ratings[:]

    for i in range(len(result)):
        sum_ratings.append(result[i]['sum_rating'])
        n_ratings.append(result[i]['n_rating'])

        rating = 0
        
        if (result[i]['n_rating']):
            rating = result[i]['sum_rating']/result[i]['n_rating']
        
        videos.append((i, result[i]['url'], rating))

    print(videos)
    print(sum_ratings)
    print(n_ratings)

    return render_template('index2.html', videos=videos)

@app.route('/getip')
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route('/validateRating', methods=['POST'])
def validateRating():
    tags =  []
    
    for i in range(len(videos)):
        tags.append(request.form['tag-'+str(i)+''])

    print("ok")

    for i in range(len(videos)):
        if tags[i] != "none":
            result = firebase.put('/videos/'+str(i)+'/', "sum_rating", int(sum_ratings[i])+int(tags[i]))
            result = firebase.put('/videos/'+str(i)+'/', "n_rating", int(n_ratings[i])+1)

    return redirect('/')

if __name__ == '__main__':
    app.run()
