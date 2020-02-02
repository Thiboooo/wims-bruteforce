import requests
from bs4 import BeautifulSoup
import json
import sys

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}
module = "U1/arithmetic/modarith.fr"
url = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session=LW3DF0081C.1&lang=fr&cmd=reply&module="+module+"&reply1=9&+useropts=4200"
nbok=0
nbnotok=0
tabstat = {}
try:
    with open('dico.json') as f:
        data = json.load(f)
        print("Fichier JSON chargé")
except:
    print("Erreur lors de l'ouverture du fichier")
    sys.exit(1)

for i in range(1,450000000):
    if(i%1000==0):
        print(str(i)+" requetes")
    if(i%500==0):
        print("Save en cours..")
        with open('dico.json', mode='w', encoding='utf-8') as f:
            json.dump(data, f)
        print("Dictionnaire sauvegardé")
        print("Stats : " + str(nbok) + " questions déjà existantes pour " + str(nbnotok) + " nouvelles questions soit " + "{0:.2f}".format(round((nbok/nbnotok),2)) +" de coeff" )
        print("------------------------------------------------------------")
        for e in tabstat.items():
            if(e[1][0] == 0):
                print(e[0]+" est surement random")
        nbok=0
        nbnotok=0
    try:
        response = requests.get(url,headers=headers)
    except:
        print("Erreur réseau")
    html = BeautifulSoup(response.content, features="html.parser")
    session_id=""
    nb_reply=1

    #récuperation de l'id de session prochaine pour bypass
    for s in html.find_all('input'):
        if(s.get("name") != None and "session" in s.get("name")):
            session_id = s.get("value")
    #récupération de l'exercice
    for p in html.find_all('h1'):
        if(p.get("class")!=None and "oeftitle" in p.get("class")):
            exercice = p.contents[0].strip()
    try:
        data[exercice]
    except:
        print("Nouvel exercice")
        data.update({exercice: {}})
    # on retire les balises identifiants mathml
    for e in html.find_all("mstyle"):
        e.replaceWith(e.text)
    #récupération de la question
    for q in html.find_all("div"):
        if(q.get("class") != None and "oefstatement" in q.get("class")):
            question=q
    try:
        data[str(exercice)][str(question)]
        #print("La question pour " + str(exercice) + " existe déjà")
        nbok+=1
        try:
            tabstat[exercice]
            tabstat[exercice].update({0 : tabstat[exercice][0]+1})
        except:
            tabstat.update({exercice: {0: 1, 1 : 0 }})
    except:        
        nbnotok+=1
        try:
            tabstat[exercice]
            tabstat[exercice].update({1 : tabstat[exercice][1]+1})
        except:
            tabstat.update({exercice: {0: 0, 1 : 1 }})
        #print("Nouvelle question pour " + str(exercice))
        #calcul du nombre de réponses a falsifier
        for s in html.find_all('input'):
            if(s.get("name") != None and "reply" in s.get("name")):
                nb_reply+=1
        # construction de l'adresse pour récupérer la reponse
        url2 = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id+"&lang=fr&cmd=reply&module="+module
        for e in range(1,nb_reply):
            url2+="&reply"+str(e)+"="+"5"
        try:
            response = requests.get(url2,headers=headers)
        except:
            print("Erreur réseau")
        #construction de la réponse et mise à jour du dictionnaire
        html = BeautifulSoup(response.content, features="html.parser")
        for rep in html.find_all("div"):
            if(rep.get("id")!=None and "answeranalysis" in rep.get("id")):
                repa = rep
        try:
            data[exercice].update({str(question) : str(repa)})
        except:
            pass
