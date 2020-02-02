import requests
from bs4 import BeautifulSoup
import json
import sys, traceback
import time
import urllib.parse

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
module = "U1/arithmetic/oeffactor.fr"
user = "marette.gauthier"
mdp = ""
# fix bug connection du à l'encodage URL
mdp = urllib.parse.quote(mdp)
headers = {'User-Agent': user_agent, "auth_user" : user, "auth_password": mdp, "cmd" : "reply", "module" : "adm/class/classes"} # cela ne sert à rien mais bon, au cas ou


# si jamais on est kick, on regénere le token à chaque fois :)
base = "http://iic0e.univ-littoral.fr/wims/wims.cgi"
baseh = BeautifulSoup(requests.get(base,headers=headers).content, features="html.parser")
for s in baseh.find_all('div'):
    if(s.get("class") != None and "wims_motd" in s.get("class")):
        u = s.find("a").get("href")
base2 = "http://iic0e.univ-littoral.fr/wims/"+u 
baseh2 = BeautifulSoup(requests.get(base2,headers=headers).content, features="html.parser")
for s in baseh2.find_all('a'):
    if(s.get("class") != None and "wims_button" in s.get("class")):
        base3 = s.get("href")
baseh3 = BeautifulSoup(requests.get(base3,headers=headers).content, features="html.parser")
for s in baseh3.find_all('input'):
    if(s.get("name") != None and "session" in s.get("name")):
        sess = s.get("value")


url = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+sess+"&lang=fr&cmd=reply&module=adm%2Fclass%2Fclasses&auth_user="+user+"&auth_password="+mdp
#load fichier
try:
    with open('dico.json') as f:
        data = json.load(f)
    print("Fichier JSON chargé\n")
except:
    print("Erreur lors de l'ouverture du fichier")
    sys.exit(1)
#connection
print("-----------------------\n")
try:
    html = BeautifulSoup(requests.get(url,headers=headers).content, features="html.parser")
except:
    print("Erreur réseau")
for s in html.find_all('div'):
    if(s.get("class") != None and "wimsbody" in s.get("class")):
        print(s.contents[14].strip()+"\n")
nbmodule=0
# selection classe
for s in html.find_all('span'):
    if(s.get("class") != None and "wims_classes_direct_course" in s.get("class")):
        nbmodule+=1
        print(str(nbmodule)+ " - " + s.text.strip()+"\n")
x = 3 #input('Quel module voulez vous choisir ? ') or 3
nbmodule=0
for s in html.find_all('span'):
    if(s.get("class") != None and "wims_classes_direct_course" in s.get("class")):
        nbmodule+=1
        if(nbmodule == int(x)):
            url2 = s.find("a").get("href")
# verif que tous les exercices soient au moins résolus une fois
try:
    html2 = BeautifulSoup(requests.get(url2,headers=headers).content, features="html.parser")
except:
    print("Erreur réseau")

print("\n--------------------\n")
for s in html2.find_all('span'):
    if(s.get("class") != None and "wims_classname" in s.get("class")):
        print(s.contents[0]+"\n")
nbmodule=0
# selection feuille
for s in html2.find_all('td'):
    if(s.get("class") != None and "wims_user_sheet_desc" in s.get("class")):
        nbmodule+=1
        print(str(nbmodule)+ " - " + s.text.strip()+"\n")
if(nbmodule==0):
    print("Vous êtes banni pendant 10 minutes.")
    sys.exit(0)
x = 1 #input('Quel feuille voulez vous choisir ? \n') or 2
nbmodule=0
for s in html2.find_all('td'):
    if(s.get("class") != None and "wims_user_sheet_desc" in s.get("class")):
        nbmodule+=1
        if(nbmodule == int(x)):
            url3 = s.find("a").get("href")
html3 = BeautifulSoup(requests.get(url3,headers=headers).content, features="html.parser")
d=False
#verification exercices
cpt=0
exos=[]
for s in html3.find_all('li'):
    if(s.get("class") != None and "wims_sheet_list" in s.get("class")):
        cpt+=1
        try:
            data[s.find("a").text]
            print(str(cpt) + " + "+s.find("a").text)
            exos.append([cpt, s.find("a").get("href"), s.find("a").text])
        except:
            print(str(cpt) + " - " + s.find("a").text + "")
            d=True

y = 10 #input("Quel exercice voulez vous choisir? (a pour tout)")
if y == "a":
    pass
else:
    if any(int(y) in i for i in exos):
        c=0
        for i,e in enumerate(exos):
            if (e[0] == int(y)):
                c=i
        url4 = [i[1] for i in exos][c]
        quality=0
        qualitya=0
        error = False
        # on veut que la qualité soit de 10
        while(quality<10 and not error):
            try: 
                # récupératuion de la question
                html4 = BeautifulSoup(requests.post(url4,headers=headers).content, features="html.parser")
                for q in html4.find_all("body"):
                    if(q.get("class") != None and "user_error" in q.get("class")):
                        error = True
                if not error:
                    for q in html4.find_all("div"):
                        if(q.get("class") != None and "oefstatement" in q.get("class")):
                            for e in html4.find_all("mstyle"):
                                e.replaceWith(e.text)
                            nomexo = [i[2] for i in exos][c]
                            try:
                                # si la question existe dans le bdd, on continue sinon nouvelle question
                                res = BeautifulSoup(data[nomexo][str(q)], features="html.parser")
                                for s in res.find_all('div'):
                                    if(s.get("class") != None and "oef_feedbacks" in s.get("class")):
                                        resfinal = s.text.replace('Une réponse possible est ','')
                                        resfinal = resfinal.replace('.','')
                                        r = resfinal
                                # cas ou la réponse n'est pas dans feedbacks mais dans un span de classe "tt"
                                try:
                                    r
                                except:
                                    for s in res.find_all('span'):
                                        if(s.get("class") != None and "tt" in s.get("class")):
                                            r = s.text
                                # fix bug où la réponse est envoyée en décodée, ce qui fait que la réponse est fausse
                                r = urllib.parse.quote(r)
                                session_id=""
                                nb_reply=1
                                #récuperation de de différentes informations pour l'injection dans l'url
                                for s in html4.find_all('input'):
                                    if(s.get("name") != None and "session" in s.get("name")):
                                        session_id = s.get("value")
                                for s in html4.find_all('input'):
                                    if(s.get("name") != None and "reply" in s.get("name")):
                                        nb_reply+=1
                                for s in html4.find_all('input'):
                                    if(s.get("name") != None and "module" in s.get("name")):
                                        module = s.get("value")
                                urlfinal = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id+"&lang=fr&cmd=reply&module="+module
                                for e in range(1,2):
                                    urlfinal+="&reply"+str(e)+"="+str(r)
                                try:
                                    print("Réponse envoyée...")
                                    html5 = BeautifulSoup(requests.post(urlfinal,headers=headers).content, features="html.parser")
                                    for q in html5.find_all("body"):
                                        if(q.get("class") != None and "user_error" in q.get("class")):
                                            error = True
                                    if not error:
                                        for s in html5.find_all('span'):
                                            if(s.get("class") != None and "oef_modulescore" in s.get("class")):
                                                print("Félicitations, "+ s.text)
                                                del r
                                        for s in html5.find_all("ul"):
                                            if(s.get("class") != None and "homeref_n4" in s.get("class")):
                                                qualitya = quality
                                                try:
                                                    quality = s.find("li").contents[2].strip().replace("Qualité : ",'')
                                                    print("Qualité actuelle :"+quality)
                                                except:
                                                    print("Erreur réponse")
                                                    sys.exit(0)
                                                quality = float(quality.replace('/10.',''))
                                                # Si jamais l'ancienne qualité est supérieur a la nouvelle, on stop tout.
                                                if(qualitya>quality):
                                                    print("Mauvaise réponse envoyée " + str(qualitya) + " nv : "+str(quality))
                                                    print("Réponse en question :"+r)
                                                    sys.exit(0)
                                    else:
                                        print("Erreur wims, vous êtes banni pendant 10mn")
                                        sys.exit(0)
                                except Exception as e: 
                                    print(traceback.print_exc())
                                    print("Erreur réseau")
                            except Exception as e: 
                                open = True
                                while(open):
                                    print("Question non trouvé dans le dictionnaire.. On suspent l'enregistrement. Attente de 25s")
                                    for s in html4.find_all('a'):
                                        if(s.get("class") != None and "scoreclose2" in s.get("class")):
                                            urls = s.get("href")
                                            open = False
                                    time.sleep(25)
                                    htmls = BeautifulSoup(requests.post(urls,headers=headers).content, features="html.parser")
                                    for q in htmls.find_all("body"):
                                        if(q.get("class") != None and "user_error" in q.get("class")):
                                            error = True
                                    if error:
                                        print("Erreur wims, vous êtes banni pendant 10mn")
                                        sys.exit(0)
                                closed = True
                                while(closed):
                                    print("Attente de 25 secondes pour activer l'enregistrement")
                                    for s in htmls.find_all('a'):
                                        if(s.get("class") != None and "scorereopen" in s.get("class")):
                                            url4 = s.get("href")
                                            closed = False
                                    time.sleep(25)
                else:
                    print("Erreur wims, vous êtes banni pendant 10mn")
                    sys.exit(0)
            except Exception as e: 
                print(traceback.print_exc())
                print("Erreur réseau")
        print("La qualité est maintenant égale à 10, bravo !")
                        
    else:
        print("Vous n'avez pas l'exercice, lancez le bruteforce avant !")