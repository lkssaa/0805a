import requests
from flask import Flask, render_template, request
import os
folder = os.getcwd()
app = Flask(__name__, template_folder=folder)

def isRus(o):
    res=False
    s='абвгдежзийклмнопрстуфухцчшщьыъэюя'
    for i in s:
        if str(o).lower() == i:
            res=True
            break 
    return res



@app.route('/')
def word():
    return render_template('templates/wordchoice.html')

@app.route('/syns', methods=['GET','POST'])
def synonyms():
    
    curr = request.args.get('wrd')
    try:
        f = open('cd.txt', 'w')

        prs = requests.get('https://jeck.ru/tools/SynonymsDictionary/'+str(curr))
        f.write(prs.text)
        f.close()
        f1 = open('cd.txt', 'r')
        data = ""
        f1.close()

        f = open('cd.txt', 'r')

        for line in f:
            if line.find("<a href='https://jeck.ru/tools/SynonymsDictionary/")!=-1:
                data+=line
        f.close()
        allA = open('refs.txt', 'w')
        allA.write(data)
        allA.close()
        allA = open('refs.txt', 'r')
        allsyn=''
        for line in allA:
            for a in line:
                if isRus(a):
                    allsyn+=a
            allsyn+='<br>'
        allSyn = open('syn.txt', 'w')
        allSyn.write(allsyn)
        allSyn.close()

        return render_template('templates/synlist.html', word=curr, sn1=allsyn)
    except IndexError:
        return render_template('templates/synlist.html', word="Синонимов на такое слово не нашлось!", sn1='')

app.run()