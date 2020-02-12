import requests
from bs4 import BeautifulSoup
import json
import sys
import traceback
import time
import urllib.parse
import numpy
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
module = "U1/arithmetic/oeffactor.fr"
user = "marette.gauthier"
mdp = ""
# fix bug connection du à l'encodage URL
mdp = urllib.parse.quote(mdp)
headers = {'User-Agent': user_agent, "auth_user": user, "auth_password": mdp,
           "cmd": "reply", "module": "adm/class/classes"}  # cela ne sert à rien mais bon, au cas ou


# si jamais on est kick, on regénere le token à chaque fois :)
base = "http://iic0e.univ-littoral.fr/wims/wims.cgi"
baseh = BeautifulSoup(requests.get(
    base, headers=headers).content, features="html.parser")
for s in baseh.find_all('div'):
    if(s.get("class") != None and "wims_motd" in s.get("class")):
        u = s.find("a").get("href")
base2 = "http://iic0e.univ-littoral.fr/wims/"+u
baseh2 = BeautifulSoup(requests.get(
    base2, headers=headers).content, features="html.parser")
for s in baseh2.find_all('a'):
    if(s.get("class") != None and "wims_button" in s.get("class")):
        base3 = s.get("href")
baseh3 = BeautifulSoup(requests.get(
    base3, headers=headers).content, features="html.parser")
for s in baseh3.find_all('input'):
    if(s.get("name") != None and "session" in s.get("name")):
        sess = s.get("value")


url = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+sess + \
    "&lang=fr&cmd=reply&module=adm%2Fclass%2Fclasses&auth_user="+user+"&auth_password="+mdp
# load fichier
# connection
print("-----------------------\n")
try:
    html = BeautifulSoup(requests.get(
        url, headers=headers).content, features="html.parser")
except:
    print("Erreur réseau")
for s in html.find_all('div'):
    if(s.get("class") != None and "wimsbody" in s.get("class")):
        print(s.contents[14].strip()+"\n")
nbmodule = 0
# selection classe
for s in html.find_all('span'):
    if(s.get("class") != None and "wims_classes_direct_course" in s.get("class")):
        nbmodule += 1
        print(str(nbmodule) + " - " + s.text.strip()+"\n")
x = 3  # input('Quel module voulez vous choisir ? ') or 3
nbmodule = 0
for s in html.find_all('span'):
    if(s.get("class") != None and "wims_classes_direct_course" in s.get("class")):
        nbmodule += 1
        if(nbmodule == int(x)):
            url2 = s.find("a").get("href")
# verif que tous les exercices soient au moins résolus une fois
try:
    html2 = BeautifulSoup(requests.get(
        url2, headers=headers).content, features="html.parser")
except:
    print("Erreur réseau")

print("\n--------------------\n")
for s in html2.find_all('span'):
    if(s.get("class") != None and "wims_classname" in s.get("class")):
        print(s.contents[0]+"\n")
nbmodule = 0
# selection feuille
for s in html2.find_all('td'):
    if(s.get("class") != None and "wims_user_sheet_desc" in s.get("class")):
        nbmodule += 1
        print(str(nbmodule) + " - " + s.text.strip()+"\n")
if(nbmodule == 0):
    print("Vous êtes banni pendant 10 minutes.")
    sys.exit(0)
x = 2  # input('Quel feuille voulez vous choisir ? \n') or 2
nbmodule = 0
for s in html2.find_all('td'):
    if(s.get("class") != None and "wims_user_sheet_desc" in s.get("class")):
        nbmodule += 1
        if(nbmodule == int(x)):
            url3 = s.find("a").get("href")
html3 = BeautifulSoup(requests.get(
    url3, headers=headers).content, features="html.parser")
d = False
# verification exercices
cpt = 0
exos = []
for s in html3.find_all('li'):
    if(s.get("class") != None and "wims_sheet_list" in s.get("class")):
        cpt += 1
        print(str(cpt) + " + "+s.find("a").text)
        exos.append([cpt, s.find("a").get("href"), s.find("a").text])

y = 9  # input("Quel exercice voulez vous choisir? (a pour tout)")
if y == "a":
    pass
else:
    if any(int(y) in i for i in exos):
        c = 0
        for i, e in enumerate(exos):
            if (e[0] == int(y)):
                c = i
        url4 = [i[1] for i in exos][c]
        quality = 0
        qualitya = 0
        error = False
        two = False
        # on veut que la qualité soit de 10
        while(quality < 10 and not error):
            try:
                # récupératuion de la question
                html4 = BeautifulSoup(requests.post(
                    url4, headers=headers).content, features="html.parser")
                for q in html4.find_all("body"):
                    if(q.get("class") != None and "user_error" in q.get("class")):
                        error = True
                if not error:
                    for q in html4.find_all("div"):
                        if(q.get("class") != None and "oefstatement" in q.get("class")):
                            for e in html4.find_all("mstyle"):
                                e.replaceWith(e.text)
                            nomexo = [i[2] for i in exos][c]
                            print(nomexo)
                            if(nomexo == 'Calculs simples modulo n'):
                                q1 = eval(str(q.contents[1]).replace('<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">', '').replace(
                                    '</math>', '').replace('−', '-').replace(')(', ')*(').replace(' ', '**').replace('×', '*'))
                                q2 = str(q.contents[2]).replace(
                                    ' modulo ', '').replace('.', '')
                                r = str(eval(str(q1)+'%'+q2))
                            elif(nomexo == 'Classes de congruences'):
                                if("sont-ils dans la même classe modulo" in q.contents[0].strip()):
                                    traiter = q.contents[0].strip().replace(' et ', ':').replace(
                                        ' sont-ils dans la même classe modulo ', ':').replace(' ?', '').split(':')
                                    q1 = eval(
                                        str(traiter[0]) + '%' + str(traiter[2]))
                                    q2 = eval(
                                        str(traiter[1]) + '%' + str(traiter[2]))
                                    if(q1 == q2):
                                        r = 'oui'
                                    else:
                                        r = 'non'
                                elif(" est-il dans la même classe de congruence modulo " in q.contents[0].strip()):
                                    traiter = q.contents[0].strip().replace("L'entier ", '').replace(
                                        ' est-il dans la même classe de congruence modulo ', ':').replace('  que ', ':').replace(' ?', '').split(':')
                                    q1 = eval(
                                        str(traiter[0]) + '%' + str(traiter[1]))
                                    q2 = eval(
                                        str(traiter[2]) + '%' + str(traiter[1]))
                                    if(q1 == q2):
                                        r = 'oui'
                                    else:
                                        r = 'non'
                                elif(" est-il un représentant de la classe " in q.contents[0].strip()):
                                    traiter = q.contents[0].strip().replace("L'entier ", '').replace(' est-il un représentant de la classe ', ':').replace(
                                        ' <math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">mod</math> ', ':').split(':')
                                    traiter2 = q.contents[2].strip().replace(
                                        " ?", '')
                                    q1 = int(traiter[0]) - int(traiter[1])
                                    q2 = eval(str(q1)+'%'+traiter2)
                                    if(q2 == 0):
                                        r = 'oui'
                                    else:
                                        r = 'non'
                                elif(" appartient-il à" in q.contents[0].strip()):
                                    q2 = str(q.contents[1]).replace('<img alt="', "").replace(
                                        ' \ZZ', ":").split(":")[0].replace(" + ", ":").split(":")
                                    q1 = q.contents[0].strip().replace(
                                        " appartient-il à", "")
                                    traitement = int(q1) - int(q2[0])
                                    if(eval(str(traitement)+"%"+str(q2[1])) == 0):
                                        r = "oui"
                                    else:
                                        r = "non"
                                else:
                                    print(q.contents[0].strip())
                                    sys.exit(0)
                            elif(nomexo == "Congruences avec un paramètre"):
                                traiter = q.contents[0].strip().replace(' et ', ':').replace(
                                    ' sont-ils dans la même classe modulo ', ':').replace(' ?', '').split(':')
                                nb1 = str(q.contents[1]).strip().replace(
                                    '<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">', '').replace('¯</math>', '')
                                mod = str(q.contents[2]).strip().replace(
                                    'modulo ', '').replace(' en fonction du chiffre', '')
                                idx = nb1.index("x")
                                if(idx == 0):
                                    x = eval('1000%'+mod)
                                    nox = eval(
                                        str(int(nb1.replace("x", "0")))+"%"+mod)
                                    r = str(x)+"x"+"+"+str(nox)
                                elif(idx == 1):
                                    x = eval('100%'+mod)
                                    nox = eval(
                                        str(int(nb1.replace("x", "0")))+"%"+mod)
                                    r = str(x)+"x"+"+"+str(nox)
                                elif(idx == 2):
                                    x = eval('10%'+mod)
                                    nox = eval(
                                        str(int(nb1.replace("x", "0")))+"%"+mod)
                                    r = str(x)+"x"+"+"+str(nox)
                                elif(idx == 3):
                                    x = eval('1%'+mod)
                                    nox = eval(
                                        str(int(nb1.replace("x", "0")))+"%"+mod)
                                    r = str(x)+"x"+"+"+str(nox)
                                r = urllib.parse.quote(r)
                            elif(nomexo == "Calculs simples dans Z/nZ"):
                                q1 = str(q.contents[1]).replace('<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">', '').replace(
                                    '</math>', '').replace('×', '*').replace('−', '-').replace(')(', ')*(').replace(' ', '**')
                                traiter = eval(q1)
                                q2 = str(q.contents[3]).replace(
                                    '<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">&amp;Zopf/', '').replace('&amp;Zopf</math>', '')
                                traiter2 = int(traiter) % int(q2)
                                r = traiter2
                            elif(nomexo == "Diviseurs de zéro II"):
                                q1 = str(q.contents[1]).replace('<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">&amp;Zopf/','').replace('&amp;Zopf</math>','')
                                res = []
                                r = ''
                                for i in range(int(q1)):
                                    if(numpy.gcd(int(q1),i) != 1 and i!=0):
                                        res.append(i)
                                for e,i in enumerate(res):
                                    if(e != len(res)-1):
                                        r+=str(i)+","
                                    else:
                                        r+=str(i)
                                r = urllib.parse.quote(r)
                            elif(nomexo == "Inverse I" or nomexo == "Inverse II"):
                                q1 = str(q.contents[0]).strip().replace("Trouver l'inverse de ",'').replace(" dans",'')
                                q2 = str(q.contents[1]).strip().replace('<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">&amp;Zopf/','').replace('&amp;Zopf</math>','')
                                r = modinv(int(q1),int(q2))
                            elif(nomexo == "Diviseurs de zéro"):
                                two = True
                                q1 = q.contents[0].strip().replace('Le nombre ', '').replace(
                                    ' est-il un diviseur de zéro dans', '')
                                q2 = str(q.contents[1]).replace(
                                    '<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">&amp;Zopf/', '').replace('&amp;Zopf</math>', '')
                                res = numpy.gcd(int(q1), int(q2))
                                if(res != 1):
                                    r = 2
                                else:
                                    r = 1
                                for s in html4.find_all('input'):
                                    if(s.get("name") != None and "session" in s.get("name")):
                                        session_id = s.get("value")
                                urlzz = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id + \
                                    "&lang=fr&cmd=reply&module=U1%2Farithmetic%2Fmodarith.fr&choice1=" + \
                                        str(r)
                                htmltmp = BeautifulSoup(requests.get(
                                    urlzz, headers=headers).content, features="html.parser")
                                for q in htmltmp.find_all("body"):
                                    if(q.get("class") != None and "user_error" in q.get("class")):
                                        error = True
                                    if not error:
                                        for s in htmltmp.find_all('span'):
                                            if(s.get("class") != None and "oef_modulescore" in s.get("class")):
                                                print(
                                                    "Félicitations, " + s.text)
                                                del r
                                        for s in htmltmp.find_all("ul"):
                                            if(s.get("class") != None and "homeref_n4" in s.get("class")):
                                                qualitya = quality
                                                try:
                                                    quality = s.find("li").contents[2].strip().replace(
                                                        "Qualité : ", '')
                                                    print(
                                                        "Qualité actuelle :"+quality)
                                                except:
                                                    print("Erreur réponse")
                                                    sys.exit(0)
                                                quality = float(
                                                    quality.replace('/10.', ''))
                                                # Si jamais l'ancienne qualité est supérieur a la nouvelle, on stop tout.
                                                if(qualitya > quality):
                                                    print(
                                                        "Mauvaise réponse envoyée " + str(qualitya) + " nv : "+str(quality))
                                                    print(urltmp)
                                                    sys.exit(0)
                            elif(nomexo == "Equation linéaire modulaire"):
                                # toujours resolvable, lol
                                two = True
                                r = str(q.contents[3]).strip().replace('\n', '').replace('<div class="wimscenter">', '').replace(' </div>', '').replace('<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">', '').replace(
                                    '</math> <img alt="equiv" src="http://iic0e.univ-littoral.fr/wims/mathfonts/100/equiv.gif" style="margin:0px; border:none"/> ', ':').replace(' mod ', ':').split(':')
                                x = int(r[0].replace('x', ''))
                                mod = int(r[2])
                                res = int(r[1])
                                sol = []
                                print("mod : " + str(mod) + " res : " +
                                      str(res) + " x :" + str(x))
                                for i in range(mod):
                                    if((x*i) % mod == res):
                                        sol.append(i)
                                print(sol)
                                for s in html4.find_all('input'):
                                    if(s.get("name") != None and "session" in s.get("name")):
                                        session_id = s.get("value")
                                if sol:
                                    urltmp = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id + \
                                        "&lang=fr&cmd=reply&module=U1%2Farithmetic%2Fmodarith.fr&choice1=2"
                                    print("ya des sol")
                                    htmltmp = BeautifulSoup(requests.get(
                                        urltmp, headers=headers).content, features="html.parser")
                                    urltmp2 = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id + \
                                        "&lang=fr&cmd=reply&module=U1%2Farithmetic%2Fmodarith.fr&reply1="
                                    for e, sols in enumerate(sol):
                                        if(e != len(sol)):
                                            urltmp2 += urllib.parse.quote(
                                                str(sols)+",")
                                        else:
                                            urltmp2 += urllib.parse.quote(
                                                str(sols))
                                    urltmp2 += "&reply2="+str(mod)
                                    print(urltmp2)
                                    htmltmp2 = BeautifulSoup(requests.get(
                                        urltmp2, headers=headers).content, features="html.parser")
                                    for q in htmltmp2.find_all("body"):
                                        if(q.get("class") != None and "user_error" in q.get("class")):
                                            error = True
                                    if not error:
                                        for s in htmltmp2.find_all('span'):
                                            if(s.get("class") != None and "oef_modulescore" in s.get("class")):
                                                print(
                                                    "Félicitations, " + s.text)
                                                del r
                                        for s in htmltmp2.find_all("ul"):
                                            if(s.get("class") != None and "homeref_n4" in s.get("class")):
                                                qualitya = quality
                                                try:
                                                    quality = s.find("li").contents[2].strip().replace(
                                                        "Qualité : ", '')
                                                    print(
                                                        "Qualité actuelle :"+quality)
                                                except:
                                                    print("Erreur réponse")
                                                    sys.exit(0)
                                                quality = float(
                                                    quality.replace('/10.', ''))
                                                # Si jamais l'ancienne qualité est supérieur a la nouvelle, on stop tout.
                                                if(qualitya > quality):
                                                    print(
                                                        "Mauvaise réponse envoyée " + str(qualitya) + " nv : "+str(quality))
                                                    sys.exit(0)
                                else:
                                    urltmp = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id + \
                                        "&lang=fr&cmd=reply&module=U1%2Farithmetic%2Fmodarith.fr&choice1=1"
                                    print("pas de sol")
                                    print(urltmp)
                                    htmltmp = BeautifulSoup(requests.get(
                                        urltmp, headers=headers).content, features="html.parser")
                                    print(htmltmp)
                                    new = ""
                                    for j in range(mod):
                                        for i in range(mod):
                                            if((x*i) % mod == j):
                                                new = j
                                    for s in htmltmp.find_all('input'):
                                        if(s.get("name") != None and "session" in s.get("name")):
                                            session_id = s.get("value")
                                            print("d'acc")
                                    print("nouvelle trouvée ! " + str(new))
                                    urltmp = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session="+session_id + \
                                        "&lang=fr&cmd=reply&module=U1%2Farithmetic%2Fmodarith.fr&reply3=" + \
                                        str(new)
                                    htmltmp = BeautifulSoup(requests.get(
                                        urltmp, headers=headers).content, features="html.parser")
                                    for q in htmltmp.find_all("body"):
                                        if(q.get("class") != None and "user_error" in q.get("class")):
                                            error = True
                                    if not error:
                                        for s in htmltmp.find_all('span'):
                                            if(s.get("class") != None and "oef_modulescore" in s.get("class")):
                                                print(
                                                    "Félicitations, " + s.text)
                                                del r
                                        for s in htmltmp.find_all("ul"):
                                            if(s.get("class") != None and "homeref_n4" in s.get("class")):
                                                qualitya = quality
                                                try:
                                                    quality = s.find("li").contents[2].strip().replace(
                                                        "Qualité : ", '')
                                                    print(
                                                        "Qualité actuelle :"+quality)
                                                except:
                                                    print("Erreur réponse")
                                                    sys.exit(0)
                                                quality = float(
                                                    quality.replace('/10.', ''))
                                                # Si jamais l'ancienne qualité est supérieur a la nouvelle, on stop tout.
                                                if(qualitya > quality):
                                                    print(
                                                        "Mauvaise réponse envoyée " + str(qualitya) + " nv : "+str(quality))
                                                    print(urltmp)
                                                    sys.exit(0)
                            else:
                                print("Exo non trouvé")
                                sys.exit(0)
                            # fix bug où la réponse est envoyée en décodée, ce qui fait que la réponse est fausse
                            session_id = ""
                            nb_reply = 1
                            # récuperation de de différentes informations pour l'injection dans l'url
                            for s in html4.find_all('input'):
                                if(s.get("name") != None and "session" in s.get("name")):
                                    session_id = s.get("value")
                            for s in html4.find_all('input'):
                                if(s.get("name") != None and "reply" in s.get("name")):
                                    nb_reply += 1
                            for s in html4.find_all('input'):
                                if(s.get("name") != None and "module" in s.get("name")):
                                    module = s.get("value")
                            if not two:
                                urlfinal = "http://iic0e.univ-littoral.fr/wims/wims.cgi?session=" + \
                                    session_id+"&lang=fr&cmd=reply&module="+module
                                for e in range(1, 2):
                                    urlfinal += "&reply"+str(e)+"="+str(r)
                                try:
                                    print("Réponse envoyée...")
                                    html5 = BeautifulSoup(requests.post(
                                        urlfinal, headers=headers).content, features="html.parser")
                                    for q in html5.find_all("body"):
                                        if(q.get("class") != None and "user_error" in q.get("class")):
                                            error = True
                                    if not error:
                                        for s in html5.find_all('span'):
                                            if(s.get("class") != None and "oef_modulescore" in s.get("class")):
                                                print(
                                                    "Félicitations, " + s.text)
                                                del r
                                        for s in html5.find_all("ul"):
                                            if(s.get("class") != None and "homeref_n4" in s.get("class")):
                                                qualitya = quality
                                                try:
                                                    quality = s.find("li").contents[2].strip().replace(
                                                        "Qualité : ", '')
                                                    print(
                                                        "Qualité actuelle :"+quality)
                                                except:
                                                    print("Erreur réponse")
                                                    sys.exit(0)
                                                quality = float(
                                                    quality.replace('/10.', ''))
                                                # Si jamais l'ancienne qualité est supérieur a la nouvelle, on stop tout.
                                                if(qualitya > quality):
                                                    print(
                                                        "Mauvaise réponse envoyée " + str(qualitya) + " nv : "+str(quality))
                                                    sys.exit(0)
                                    else:
                                        print(
                                            "Erreur wims, vous êtes banni pendant 10mn")
                                        sys.exit(0)
                                except Exception as e:
                                    print(traceback.print_exc())
                                    print("Erreur réseau")
                else:
                    print("Erreur wims, vous êtes banni pendant 10mn")
                    sys.exit(0)
            except Exception as e:
                print(traceback.print_exc())
                print("Erreur réseau")
        print("La qualité est maintenant égale à 10, bravo !")

    else:
        print("Vous n'avez pas l'exercice, lancez le bruteforce avant !")
