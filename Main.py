from flask import Flask, render_template, request, redirect, session, json, jsonify, url_for
import sys
import socnet as sn
from math import inf, isinf
from queue import Queue
from random import randint
import requests


app = Flask(__name__)



sn.graph_width = 400
sn.graph_height = 225
sn.edge_width = 1

    
###  Importar grafos dos topicos ####

historia_gr = sn.load_graph('../historia.gml', has_pos=False)
cultura_gr = sn.load_graph('../cutura.gml', has_pos=False)
dieta_gr = sn.load_graph('../dieta.gml', has_pos=False)
lingua_gr = sn.load_graph('../lingua.gml', has_pos=False)
loc_pop_gr = sn.load_graph('../loc_pop.gml', has_pos=False)
religiao_gr = sn.load_graph('../religiao.gml', has_pos=False)

### func de PageRank ###

for n in geral.nodes():
    geral.node[n]['pagerank'] = 0
    
def equals(a, b):
    return abs(a - b) < 0.000000001


def calculate_pagerank(g):
    length = g.number_of_nodes()

    k = 10
    scale = 0.8
    residue = (1 - scale) / length

    R = sn.build_matrix(g)

    for n in g.nodes:
        total = np.sum(R[n,])

        if equals(total, 0):
            R[n, n] = 1
        else:
            R[n,] /= total

    R = scale * R + residue

    Rt = R.transpose()

    rank = 1 / length

    r = np.full((length, 1), rank)

    for _ in range(k):
        r = Rt.dot(r)

    for n in g.nodes:
        g.nodes[n]['pagerank'] = r[n, 0]

### func de vizinhos ###

def links(g, trib):
    
    for n in g.nodes():
        if g.node[n]['nome'] == trib:
            
            vizinhos = []
            for m in g.neighbors(n):
                vizinhos.append(m)
    
    temp = random.sample(set(vizinhos), 2)
    
    ans = []
    for num in temp:
        
        ans.append(g.node[num]['nome'])
        
    return ans
  
### Func de adicionar arestas ###
    
def add_edge(g, n, m):
    g.add_edge(n,m)
    g.edges[n,m]['color'] = (0,0,0)


### Organizar Grafos e dar nomes aos nós ###

topicos = [historia_gr, cultura_gr, dieta_gr, lingua_gr, loc_pop_gr, religiao_gr]

tribos = ['guaranis', 'caingangue', 'pataxos', 
          'caetes', 'caiapos', 'guajajaras', 
          'ianomamis', 'potiguaras', 'macuxi', 'marubos','tapuias', 'terenas', 'ticunas', 'xavantes' ]

for t in topicos:
    for n in t.nodes():
        t.node[n]['nome'] = tribos[n]
        
###  Ligações de arestas ###

for t in topicos:
    for n in t.nodes():
        for m in t.nodes():
            
            x = randint(0,50)

            if x > 45 and n != m:
                add_edge(t, n, m)
    
    
    for s in t.nodes():
        
        v = []
        
        for m in t.neighbors(s):
            v.append(m)
            
        if len(v) < 2:
            
            some_node = randint(0,13)
            add_edge(t, s, some_node)
            
            some_other_node = randint(0,13)
            add_edge(t, s, some_other_node)
            




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

    cultura1 = request.form['cultura-1'] != None
    cultura2 = request.form['cultura-2'] != None
    cultura3 = request.form['cultura-3'] != None
    cultura4 = request.form['cultura-4'] != None
    cultura5 = request.form['cultura-5'] != None
    cultura6 = request.form['cultura-6'] != None 
    cultura7 = request.form['cultura-7'] != None
    cultura8 = request.form['cultura-8'] != None
    
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
        tribos_dict['guaranis'] +=1
        tribos_dict['tapuias'] +=1
    elif lingua == 3:
        tribos_dict['pataxos'] +=1
    elif lingua == 4:
        tribos_dict['terena'] +=1
    elif lingua == 5:
        tribos_dict['ticunas'] +=1
    elif lingua == 6:
        tribos_dict['marubos'] +=1

    
    if cultura1 == True:
        tribos_dict['tapuias'] +=1
    if cultura2 == True:
        tribos_dict['caetes'] +=1
    if cultura3 == True:
        tribos_dict['xavantes'] +=1
        tribos_dict['tapuias'] +=1
    if cultura4 == True:
        tribos_dict['guaranis'] +=1
        tribos_dict['marubos'] +=1
    if cultura5 == True:
        tribos_dict['guaranis'] +=1
    if cultura6 == True:
        tribos_dict['macuxi'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['xavantes'] +=1
    if cultura7 == True:
        tribos_dict['xavantes'] +=1
        tribos_dict['terena'] +=1
    if cultura8 == True:
        tribos_dict['caiapos'] +=1
        tribos_dict['caingangue'] +=1

    print(str(max(tribos_dict, key=tribos_dict.get)))
    return redirect('/'+ str(max(tribos_dict, key=tribos_dict.get))+'')

@app.route('/caetes')
def caetes():
    return render_template('caetes.html')

@app.route('/caiapos')
def caiapos():
    return render_template('caiapos.html')

@app.route('/caingangue')
def caingangue():
    return render_template('caingangue.html')

@app.route('/guajajaras')
def guajajaras():
    return render_template('guajajaras.html')

@app.route('/guaranis')
def guaranis():
    return render_template('guaranis.html')

@app.route('/ianomamis')
def ianomamis():
    return render_template('ianomamis.html')

@app.route('/macuxi')
def macuxi():
    return render_template('macuxi.html')

@app.route('/marubos')
def marubos():
    return render_template('marubos.html')

@app.route('/pataxos')
def pataxos():
    return render_template('pataxos.html')

@app.route('/potiguaras')
def potiguaras():
    return render_template('potiguaras.html')

@app.route('/tapuias')
def tapuias():
    return render_template('tapuias.html')

@app.route('/terenas')
def terenas():
    return render_template('terenas.html')

@app.route('/ticunas')
def ticunas():
    return render_template('ticunas.html')

@app.route('/xavantes')
def xavantes():
    return render_template('xavantes.html')



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
