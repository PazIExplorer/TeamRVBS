from app import app
from flask import render_template, request, make_response, redirect, url_for
from werkzeug import secure_filename
import mysql.connector

import os
from app.pythonScript import pdfgen
from app.pythonScript import excelGen
from app.pythonScript import fonctionPy
from app.pythonScript import mdpGen


cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
cursor = cnx.cursor()
cursora = cnx.cursor()
cursorb = cnx.cursor()

# Vérification de la validité du cookie
def cookieEstValide():
    # Vérification de connexion déjà valable (cookies)
    if ('compteConnecte' in request.cookies) and ('typeCompte' in request.cookies):
        # On vérifie que le compte est un compte valide
        user_name = request.cookies.get('compteConnecte')
        user_accType = request.cookies.get('typeCompte')
        query = ("SELECT identifiant FROM connexion WHERE identifiant=%s AND typeCompte=%s")
        val = (user_name, user_accType)
        cursor.execute(query, val)
        user_result = cursor.fetchall()

        if len(user_result) != 0:
            # Cookie correct
            return True

    # Cookie incorrect
    return False


# Vérification que le compte connecté est administrateur
def compteEstAdmin():
    if 'typeCompte' in request.cookies:
        if request.cookies.get('typeCompte') == "administrateur":
            return True
    
    # Non connecté ou non admin
    return False



@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():


    if cookieEstValide():
        return redirect("choixFiliere")
        
    
    # CONNEXION
    if request.method == "POST":
        
        #--------------------
        # Voir la connexion a partir de la bdd
        #--------------------
        
        user_name = request.form["user_name"]
        user_mdp = request.form["user_mdp"]

        query = ("SELECT * FROM connexion WHERE identifiant=%s AND motdepasse=%s")
        val = (user_name,user_mdp)
        cursor.execute(query, val)
        user_result = cursor.fetchall()

        if len(user_result) == 0:
            # ID / MDP Incorrect
            return render_template('index.html', connexionError=True)

        else:
            # ID et MDP Correct
            res = make_response(render_template("choixFiliere.html"))
            res.set_cookie('compteConnecte', user_result[0][0], max_age=60*60*24)

            res.set_cookie('typeCompte', user_result[0][2], max_age=60*60*24) # Type de compte: "administrateur" ou "enseignant"
            return res
        
    # PAGE D'INDEX
    return render_template('index.html')


@app.route("/deconnexion", methods=["GET"])
def deconnexion():
    if 'compteConnecte' in request.cookies:
        res = make_response(render_template('deconnexion.html'))
        res.set_cookie('compteConnecte', "null", max_age=0)
        res.set_cookie('typeCompte', "null", max_age=0)
        return res
    else:
        return redirect("index")

@app.route("/choixFiliere", methods=["GET","POST"])
def choixFiliere():

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    if request.method == "POST":
        tabSemA = request.form["tsa"]
        
        print("tabAlternant"+tabSemA)

    return render_template("choixFiliere.html")


@app.route("/pageGenerale")
def pageGenerale():

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    etu = cursor.fetchall()
    for e in etu:
        print(str(e[0]))



    query = ("SELECT * FROM presence")
    cursor.execute(query)
    presence = cursor.fetchall()
    
    #génération du excel a chaque fois qu'on est sur la page générale
    excelGen.creation()
    return render_template("pageGenerale.html",user=etu,presence=presence)


@app.route("/pageEtu/<id>", methods=["GET", "POST"])
def pageEtu(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    id=id
    if request.method == "POST":
        #idCarteEtu = int(request.form["idCarteEtu"],16)
        #print("idCarteEtu => "+str(idCarteEtu))
        #idC = idCarteEtu
        #print("idCarte= "+str(idC))
        idCarteEtu = id
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        numeroEtudiant = int(request.form["numeroEtudiant"])
        typeContratEtudiant = request.form["typeContratEtudiant"]
        tarif = float(request.form["tarif"])
        filiere = int(request.form["filiere"])
        numeroTel = int(request.form["numeroTel"])
        mailEtu = request.form["mailEtu"]
        mailEntreprise = request.form["mailEntreprise"]	
        
        #print(idCarteEtu)
        #print(nom)
        #print(prenom)
        querya = ("UPDATE etudiant SET idCarteEtu=%s,nom=%s,prenom=%s,numeroEtudiant=%s,typeContratEtudiant=%s,tarif=%s,filiere=%s,numeroTel=%s,mailEtu=%s,mailEntreprise=%s WHERE idCarteEtu=%s")
        val = (idCarteEtu,nom,prenom,numeroEtudiant,typeContratEtudiant,tarif,filiere,numeroTel,mailEtu,mailEntreprise,id)
        
        queryb = ("UPDATE presence SET idCarteEtu=%s WHERE idCarteEtu=%s")
        valb = (idCarteEtu,id)
	#querya = ("UPDATE etudiant SET nom = %s WHERE idCarteEtu=%s")
        #val = (nom,id)
        print("1")
        try:
            print("3")
            cursora.execute(querya,val)
            #cursorb.execute(queryb,valb)
            cnx.commit()
            print("2")
            
            querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
            cursora.execute(querya)
            etu = cursora.fetchall()
            print("4")

            queryb = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
            cursorb.execute(queryb)
            presence = cursorb.fetchall()
            print("5")

            return render_template("pageEtu.html",user=etu,presence=presence)
        
        except:
            print("except")
            cnx.rollback()
        
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()
 
    
    queryb = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursorb.execute(queryb)
    presence = cursorb.fetchall()

    return render_template("pageEtu.html", user=etu , presence=presence)

@app.route("/pageConvention/<id>", methods=["GET", "POST"])
def pageConvention(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))


    id=id
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()

    if request.method == "POST":
        conv = request.files["conv"]
        #print(secure_filename(conv.filename))
        #nom_conv = '{{etu[0][1]}}_{{etu[0][2]}}_convention.pdf'
        non_conv = secure_filename(conv.filename)
        conv.save('/root/TeamRVBS/app/static/convention/'+non_conv)
    
    return render_template("pageConvention.html",user=etu)




@app.route("/pageModifEtu/<id>")
def pageModifEtu(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    id=id
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()

    querya = ("SELECT * FROM filiere")
    cursora.execute(querya)
    filiere = cursora.fetchall()
    #etu[0][0]= hex(etu[0][0])
    return render_template("pageModifEtu.html", user=etu, fil=filiere)

@app.route("/pdfEtuPresence/<id>")
def pdfEtuPresence(id): 

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))


    id=id
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()

    querya = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][6]))
    cursora.execute(querya)
    filiere = cursora.fetchall()

    querya = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    presence = cursora.fetchall()

    myPresence= pdfgen.presence(etu[0][1]+" "+etu[0][2],filiere[0][1],presence)
    return render_template("pdfEtu.html",myPresence=myPresence,user=etu)

@app.route("/pdfEtu/<id>")
def pdfEtu(id): 

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    id=id 
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()

    querya = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    presence = cursora.fetchall()

    querya = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][6]))
    cursora.execute(querya)
    filiere = cursora.fetchall()
    #etu= Etudiant.query.get(int(id))
    #filiere=Filiere.query.get(int(etu.filiere))
    myPDF=pdfgen.pdf(etu[0][1]+" "+etu[0][2],filiere[0][1],presence)
    return render_template("pdfEtu.html",myPDF=myPDF,user=etu)

@app.route("/archiveEtu/<id>")
def archiveEtu(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    import re
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()
    eturegex=rf".*{etu[0][1]}\s{etu[0][2]}.*"

    folderContent = os.listdir(os.path.join("./app/static/archive"))
    fichiersEtu = []

    for i in folderContent:
        if (re.match(eturegex,i)!=None):
            fichiersEtu.append(i)
    print(fichiersEtu)

    return render_template("archiveEtu.html",user=etu, folderContent=fichiersEtu) 

@app.route("/ajoutEtu/<nomprenomid>",methods=["GET","POST"])
def ajoutEtu(nomprenomid):
    np = str(nomprenomid).split('-')
    idCarte = int(np[2])
    nom = np[0]
    prenom = np[1]
    numEtu = np[3]
    query = ("INSERT INTO etudiant (idCarteEtu,nom,prenom,numeroEtudiant) VALUES (%s,%s,%s,%s)")
    arg = (idCarte,nom,prenom,numEtu)
    try:
        cursor.execute(query,arg)
        cnx.commit()
        return render_template("success.html")
    except Exception as e:
        print(e)
        return render_template("failure.html")

@app.route("/pageAdministration", methods=["GET", "POST"])
def pageAdministration():
    
    if request.method == "POST":
       
        
        debutAnnee = request.form["debutAnnee"]
        finAnnee = request.form["finAnnee"]
        debutAffiche = request.form["debutPeriode"]
        finAffiche = request.form["finPeriode"]
        presidentSMB = request.form["presidentUSMB"]
        presidentSFC = request.form["presidentSFC"]
        tarifMaster = int(request.form["tarifMaster"])

       
        print("test")
        print(debutAnnee)
        print("test")
        print("test")
        print(finAnnee)
        print("test")
        print("test")
        print(debutAffiche)
        print("test")
        print("test")
        print(finAffiche)
        print("test")
        print("test")
        print(presidentSMB)
        print("test")
        print("test")
        print(presidentSFC)
        print("test")
        print("test")
        print(tarifMaster)
        print("test")

        query = ("UPDATE administration SET debutAnnee=%s,finAnnee=%s,debutAffiche=%s,finAffiche=%s,presidentSMB=%s,presidentSFC=%s,tarfiMaster=%s")
        val = (debutAnnee,finAnnee,debutAffiche,finAffiche,presidentSMB,presidentSFC,tarifMaster)

        print("1")
        try:
            print("3")
            cursora.execute(query,val)
           
            querya = ("SELECT * FROM administration" )
            cursora.execute(querya)
            admin = cursora.fetchall()
            print(admin)
            print("4")


            return render_template("pageAdministration.html",admin=admin)
        
        except:
            print("ALED")
            cnx.rollback()
        
    querya = ("SELECT * FROM administration ")
    cursora.execute(querya)
    admin = cursora.fetchall()
    print(admin)
 
    return render_template("pageAdministration.html",admin=admin)


@app.route("/emploiDuTemps")
@app.route("/emploiDuTemps", methods=['GET', 'POST'])
def emploiDuTempsPicker():
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")

    if request.method == 'POST':

        data = request.form['hide']
        if data:
            print("TEST route.py")
            print(data)
            fonctionPy.sendEmploiDuTemps(data)

    fonctionPy.recupererEmploiDuTemps()
    return render_template("emploiDuTempsPicker.html")
@app.route("/administration")
def administration():
    return render_template("administration.html")


@app.route("/creationCompte", methods=['GET', 'POST'])
def creationCompte():
    if request.method == "POST":
        email = request.form["nomCompte"]
        mdp = mdpGen.generateurMDP()
        typeCompte = request.form["type"]
        querya = ("INSERT INTO connexion VALUES(%s,%s,%s)")
        val =(email,mdp,typeCompte)
        try:
            cursora.execute(querya,val)
            cnx.commit()
            print("mail = "+email)
            print("mdp = "+mdp)
            print("type = "+typeCompte)
            mdpGen.envoiMail(email,mdp)
            #return "Compte créé avec succès"
            return render_template("choixFiliere.html")
        except:
            print("except")
            cnx.rollback()
            #return "Echec lors de la création du compte. Veuillez réessayer"
            return render_template("creationCompte.html")

    return render_template("creationCompte.html")

@app.route("/gestionCompte", methods=['GET', 'POST'])
def gestionCompte():
    if request.method == "POST":
        nom = request.form["nomCompte"]
        mdp = request.form["mdp"]
        
        querya = ("UPDATE connexion SET motdepasse=%s WHERE identifiant=%s")
        val = (mdp,nom)
        try:
            cursora.execute(querya,val)
            cnx.commit()
            #return "Compte modifié avec succès"
            return render_template("choixFiliere.html")
        except:
            print("except")
            cnx.rollback()
            #return "Echec lors de la modification du compte. Veuillez réessayer"
            return render_template("gestionCompte.html")

    return render_template("gestionCompte.html")

