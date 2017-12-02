from flask import Flask, render_template, request, redirect, session, json, jsonify, url_for
import requests
import uuid
import os
from firebase import firebase

firebase = firebase.FirebaseApplication('https://insper-sna.firebaseio.com', None)



videos = []
sum_ratings = []
n_ratings = []

app = Flask(__name__)

@app.route('/youInsper')
def hello():
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
    
    sorted_videos = sorted(videos, key=lambda tup: tup[2], reverse=True)

    return render_template('index.html', videos=sorted_videos)

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
