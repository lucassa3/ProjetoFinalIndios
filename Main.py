from flask import Flask, render_template, request, redirect, session, json, jsonify, url_for
import sys
import socnet as sn
from math import inf, isinf
from queue import Queue
import numpy as np
import random
import requests
from operator import itemgetter


app = Flask(__name__)

    
###  Importar grafos dos topicos ####

historia_gr = sn.load_graph('historia.gml', has_pos=False)
cultura_gr = sn.load_graph('cultura.gml', has_pos=False)
dieta_gr = sn.load_graph('dieta.gml', has_pos=False)
lingua_gr = sn.load_graph('lingua.gml', has_pos=False)
loc_pop_gr = sn.load_graph('loc_pop.gml', has_pos=False)
religiao_gr = sn.load_graph('religiao.gml', has_pos=False)
geral_gr = sn.load_graph('geral.gml', has_pos=False)

### func de PageRank ###

for n in geral_gr.nodes():
    geral_gr.node[n]['pagerank'] = 0
    
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

topicos = [historia_gr, cultura_gr, dieta_gr, lingua_gr, loc_pop_gr, religiao_gr, geral_gr]

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
            
            x = random.randint(0,50)

            if x > 45 and n != m:
                add_edge(t, n, m)
    
    
    for s in t.nodes():
        
        v = []
        
        for m in t.neighbors(s):
            v.append(m)
            
        if len(v) < 2:
            
            some_node = random.randint(0,13)
            add_edge(t, s, some_node)
            
            some_other_node = random.randint(0,13)
            add_edge(t, s, some_other_node)



calculate_pagerank(geral_gr)

for n in geral_gr.nodes():
    print(geral_gr.nodes[n]['pagerank'])

def remove_node_name(g, node_name):
    for n in g.nodes():
        if g.node[n]['nome'] == node_name:
            print(g.node[n]['nome'])
            g.remove_node(n)
            break





        
tribos_dict = {'caetes': 0, 'caiapos': 0, 'caingangue': 0, 'guajajaras': 0, 'guaranis': 0, 'ianomamis': 0, 'macuxi': 0, 'marubos': 0, 'pataxos': 0, 'potiguaras': 0, 'tapuias': 0, 'terenas': 0, 'ticunas': 0, 'xavantes': 0}
total_dict = {'caetes': 0, 'caiapos': 0, 'caingangue': 0, 'guajajaras': 0, 'guaranis': 0, 'ianomamis': 0, 'macuxi': 0, 'marubos': 0, 'pataxos': 0, 'potiguaras': 0, 'tapuias': 0, 'terenas': 0, 'ticunas': 0, 'xavantes': 0}

def pagerank_answers(g):
    global tribos_dict
    global total_dict
    for n in g.nodes():
        total_dict[str(g.node[n]['nome'])] = g.node[n]['pagerank'] + (tribos_dict[str(g.node[n]['nome'])]/100)
        print(total_dict[str(g.node[n]['nome'])])
    
    newA = sorted(total_dict, key=total_dict.get, reverse=True)[:2]
    return newA





@app.route('/')
def quiz():
    global tribos_dict
    tribos_dict = dict.fromkeys(tribos_dict, 0)

    return render_template('quiz.html')

@app.route('/validateQuiz', methods = ["POST"])
def validateQuiz():
    global tribos_dict
    historia = int(request.form['Historia'])
    lingua = int(request.form['Lingua'])

    
    cultura1 = request.form.get('check1')
    cultura2 = request.form.get('check2')
    cultura3 = request.form.get('check3') 
    cultura4 = request.form.get('check4') 
    cultura5 = request.form.get('check5') 
    cultura6 = request.form.get('check6') 
    cultura7 = request.form.get('check7')
    cultura8 = request.form.get('check8')
    
    religiao = int(request.form['Religiao'])
    locpop = int(request.form['Localizacao'])
    dieta = int(request.form['Dieta'])


    if lingua == 1:
        tribos_dict['caiapos'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['xavantes'] +=1
    elif lingua == 2:
        tribos_dict['caetes'] +=1
        tribos_dict['guajajaras'] +=1
        tribos_dict['guaranis'] +=1
        tribos_dict['tapuias'] +=1
    elif lingua == 3:
        tribos_dict['pataxos'] +=1
    elif lingua == 4:
        tribos_dict['terenas'] +=1
    elif lingua == 5:
        tribos_dict['ticunas'] +=1
    elif lingua == 6:
        tribos_dict['marubos'] +=1

    
    if cultura1:
        tribos_dict['tapuias'] +=1
    if cultura2:
        tribos_dict['caetes'] +=1
    if cultura3:
        tribos_dict['xavantes'] +=1
        tribos_dict['tapuias'] +=1
    if cultura4:
        tribos_dict['guaranis'] +=1
        tribos_dict['marubos'] +=1
    if cultura5:
        tribos_dict['guaranis'] +=1
    if cultura6:
        tribos_dict['macuxi'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['xavantes'] +=1
    if cultura7:
        tribos_dict['xavantes'] +=1
        tribos_dict['terenas'] +=1
    if cultura8:
        tribos_dict['caiapos'] +=1
        tribos_dict['caingangue'] +=1

    if dieta == 1:
        tribos_dict['macuxi'] +=1
    elif dieta == 2:
        tribos_dict['tapuias'] +=1
        tribos_dict['ianomamis'] +=1
        tribos_dict['guaranis'] +=1
        tribos_dict['ticunas'] +=1
        tribos_dict['xavantes'] +=1
    elif dieta == 3:
        tribos_dict['potiguaras'] +=1
        tribos_dict['terenas'] +=1
    elif dieta == 4:
        tribos_dict['pataxos'] +=1
    elif dieta == 5:
        tribos_dict['caetes'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['guajajaras'] +=1
        tribos_dict['marubos'] +=1
        tribos_dict['caiapos'] +=1

    if historia == 1:
        tribos_dict['caetes'] +=1
        tribos_dict['caingangue'] +=1
        tribos_dict['ticunas'] +=1
        tribos_dict['tapuias'] +=1
        tribos_dict['terenas'] +=1
    elif historia == 2:
        tribos_dict['guajajaras'] +=1
        tribos_dict['macuxi'] +=1
        tribos_dict['pataxos'] +=1
        tribos_dict['caiapos'] +=1        
    elif historia == 3:
        tribos_dict['potiguaras'] +=1
        tribos_dict['guaranis'] +=1
    elif historia == 4:
        tribos_dict['ianomamis'] +=1
        tribos_dict['marubos'] +=1
        tribos_dict['xavantes'] +=1


    if religiao == 1:
        tribos_dict['caingangue'] +=1
        tribos_dict['pataxos'] +=1
        tribos_dict['xavantes'] +=1
        tribos_dict['potiguaras'] +=1
    elif religiao == 2:
        tribos_dict['guaranis'] +=1
        tribos_dict['guajajaras'] +=1
        tribos_dict['xavantes'] +=1
    elif religiao == 3:
        tribos_dict['ianomamis'] +=1
        tribos_dict['potiguaras'] +=1
        tribos_dict['terenas'] +=1
        tribos_dict['marubos'] +=1
        tribos_dict['guaranis'] +=1
    elif religiao == 4:
        tribos_dict['tapuias'] +=1
        tribos_dict['marubos'] +=1
        tribos_dict['macuxi'] +=1
    elif religiao == 5:
        tribos_dict['caiapos'] +=1
        tribos_dict['marubos'] +=1

    if locpop ==1:
        tribos_dict['guajajaras'] +=1
        tribos_dict['ianomamis'] +=1
        tribos_dict['macuxi'] +=1
        tribos_dict['marubos'] +=1
        tribos_dict['ticunas'] +=1
    elif locpop == 2:
        tribos_dict['potiguaras'] +=1
        tribos_dict['pataxos'] +=1
        tribos_dict['tapuias'] +=1
    elif locpop == 3:
        tribos_dict['caiapos'] +=1
        tribos_dict['guaranis'] +=1
        tribos_dict['terenas'] +=1
        tribos_dict['xavantes'] +=1
    elif locpop == 4:
        tribos_dict['caingangue'] +=1
        tribos_dict['guaranis'] +=1
    elif locpop == 5:
        tribos_dict['guaranis'] +=1
        tribos_dict['caingangue'] +=1
    
    oi = str(max(tribos_dict, key=tribos_dict.get))
    #remove_node_name(geral_gr, oi)
        

    print(str(max(tribos_dict, key=tribos_dict.get)))
    return redirect('/'+ str(max(tribos_dict, key=tribos_dict.get))+'')

@app.route('/caetes')
def caetes():

    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('caetes.html', r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/caiapos')
def caiapos():

    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('caiapos.html', r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/caingangue')
def caingangue():

    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)


    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('caingangue.html', r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/guajajaras')
def guajajaras():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('guajajaras.html', r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/guaranis')
def guaranis():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('guaranis.html', r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/ianomamis')
def ianomamis():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('ianomamis.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/macuxi')
def macuxi():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('macuxi.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/marubos')
def marubos():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('marubos.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/pataxos')
def pataxos():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('pataxos.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/potiguaras')
def potiguaras():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('potiguaras.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/tapuias')
def tapuias():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('tapuias.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/terenas')
def terenas():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('terenas.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/ticunas')
def ticunas():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)

    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('ticunas.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)

@app.route('/xavantes')
def xavantes():
    calculate_pagerank(geral_gr)
    r_geral =  pagerank_answers(geral_gr)
    
    r_historia = links(historia_gr, 'caingangue')
    r_lingua = links(lingua_gr, 'caingangue')
    r_cultura = links(cultura_gr, 'caingangue')
    r_religiao = links(religiao_gr, 'caingangue')
    r_locpop = links(loc_pop_gr, 'caingangue')
    r_dieta = links(dieta_gr, 'caingangue')
    return render_template('xavantes.html',r_geral=r_geral, r_historia=r_historia,  r_lingua=r_lingua, r_cultura=r_cultura, r_religiao=r_religiao, r_locpop=r_locpop, r_dieta=r_dieta)


if __name__ == '__main__':
    app.run()
