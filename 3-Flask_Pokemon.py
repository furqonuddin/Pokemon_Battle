from flask import Flask, render_template, jsonify, make_response, request, send_from_directory, redirect, url_for
import json
import requests
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import random


app = Flask(__name__)

# =============================================================
@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/hasil', methods = ['POST', 'GET'])
def hasil():
    try:
        name1 = request.form['name1'].capitalize()
        name2 = request.form['name2'].capitalize()
        # url = 'https://pokeapi.co/api/v2/pokemon/'
        
        df = pd.read_csv('pokemon.csv')
        model = joblib.load('modelML')
        try:
            if name1 == "":
                return render_template('error.html')

            else:
                url = 'https://pokeapi.co/api/v2/pokemon/' + name1.lower()
                url2 = 'https://pokeapi.co/api/v2/pokemon/' + name2.lower()
                pokemon1 = requests.get(url)
                pokemon2 = requests.get(url2)
                id1 = pokemon1.json()["id"]
                id2 = pokemon2.json()["id"]
                foto1 = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/"+str(id1)+".png"
                foto2 = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/"+str(id2)+".png"


                #Prediksi value
                # ==========================================================
                # idpoke1, idpoke2, hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef2, speed1, speed2, winner
                id1 = df['#'][df['Name'] == name1].values[0]
                hp1 = df['HP'][df['Name']==name1].values[0]
                att1 = df['Attack'][df['Name']==name1].values[0]
                def1 = df['Defense'][df['Name']==name1].values[0]
                spatt1 = df['Sp. Atk'][df['Name']==name1].values[0]
                spdef1 = df['Sp. Def'][df['Name']==name1].values[0]
                speed1 = df['Speed'][df['Name']==name1].values[0]

                id2 = df['#'][df['Name'] == name2].values[0]
                hp2 = df['HP'][df['Name']==name2].values[0]
                att2 = df['Attack'][df['Name']==name2].values[0]
                def2 = df['Defense'][df['Name']==name2].values[0]
                spatt2 = df['Sp. Atk'][df['Name']==name2].values[0]
                spdef2 = df['Sp. Def'][df['Name']==name2].values[0]
                speed2 = df['Speed'][df['Name']==name2].values[0]

                # pokemon1,pokemon2,winner,HP2,Attack2,Defense2,Sp. Atk2,Sp. Def2,Speed2,HP,Attack,Defense,Sp. Atk,Sp. Def,Speed
                prediksi = model.predict([[hp2, att2, def2, spatt2, spdef2, speed2, hp1, att1, def1,  spatt1,  spdef1,  speed1]])
                proba = model.predict_proba([[hp2, att2, def2, spatt2, spdef2, speed2, hp1, att1, def1,  spatt1,  spdef1,  speed1]])
                maxproba = proba[0].max()*100

                if prediksi[0] == 1:
                    hasilpred = name2
                else:
                    hasilpred = name1

                # print(hasilpred)


                # Plot =====================
                listnama = [name1, name2]

                listHP = []
                listAttack = []
                listDef = []
                listSpatck = []
                listspdef = []
                listspeed = []

                for i in listnama:
                    listHP.append(df['HP'][df['Name']==i].values[0])
                for i in listnama:
                    listAttack.append(df['Attack'][df['Name']== i].values[0])
                for i in listnama:
                    listDef.append(df['Defense'][df['Name']== i].values[0])
                for i in listnama:
                    listSpatck.append(df['Sp. Atk'][df['Name']== i].values[0])
                for i in listnama:
                    listspdef.append(df['Sp. Def'][df['Name']== i].values[0])
                for i in listnama:
                    listspeed.append(df['Speed'][df['Name']== i].values[0])

                plt.clf()
                plt.figure(figsize=(10, 6))

                plt.subplot(161)
                plt.bar(listnama, listHP, color='br')
                plt.xticks(rotation=90)
                plt.title('HP')

                plt.subplot(162)
                plt.bar(listnama, listAttack, color='br')
                plt.xticks(rotation=90)
                plt.title('Attack')

                plt.subplot(163)
                plt.bar(listnama, listDef, color='br')
                plt.xticks(rotation=90)
                plt.title('Defense')

                plt.subplot(164)
                plt.bar(listnama, listSpatck, color='br')
                plt.xticks(rotation=90)
                plt.title('Sp Attack')

                plt.subplot(165)
                plt.bar(listnama, listspdef, color='br')
                plt.xticks(rotation=90)
                plt.title('Sp Defense')

                plt.subplot(166)
                plt.bar(listnama, listspeed, color='br')
                plt.xticks(rotation=90)
                plt.title('Speed')


                xy = random.randint(100, 10000)
                listplot = os.listdir('./storage')
                lis = str(len(listplot) + 1) + '_' + str(xy) + '.jpg'

                plt.savefig('storage/%s' % lis)
                

                return render_template('hasil.html', a1=name1, a2=name2, zz=lis,  e=foto2, f=foto1, p=hasilpred, prob=maxproba)

        except():
            return redirect(url_for('error'))

    except():
        return redirect(url_for('error'))


@app.route('/grafik/<path:yy>')                                 # nama path untuk diakses dari web
def grafik(yy):
    return send_from_directory('storage', yy)

@app.route('/error')
def error():
    return render_template('error.html')

# not found display
@app.errorhandler(404)
def tidakfound(error):                                                 
    return make_response('<h1>NOT FOUND (404)</h1>')


if __name__ == '__main__':
    app.run(debug = True) 