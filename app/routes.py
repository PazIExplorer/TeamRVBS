# -*-coding:utf-8 -*

from app import app
from flask import render_template, request, make_response, redirect, url_for
from werkzeug import secure_filename
import mysql.connector

import os.path
from os import path


import os
from app.pythonScript import pdfgen
from app.pythonScript import excelGen
from app.pythonScript import fonctionPy
from app.pythonScript import mdpGen

from app.pythonScript import config

# Vérification de la validité du cookie
def cookieEstValide():
    # Vérification de connexion déjà valable (cookies)
    if ('compteConnecte' in request.cookies) and ('typeCompte' in request.cookies):
        # On vérifie que le compte est un compte valide
        user_name = request.cookies.get('compteConnecte')
        user_accType = request.cookies.get('typeCompte')

        cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
        cursor = cnx.cursor()

        query = ("SELECT identifiant FROM connexion WHERE identifiant=%s AND typeCompte=%s")
        val = (user_name, user_accType)
        cursor.execute(query, val)
        user_result = cursor.fetchall()

        cnx.close()

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

        cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
        cursor = cnx.cursor()

        query = ("SELECT * FROM connexion WHERE identifiant=%s AND motdepasse=%s")
        val = (user_name,user_mdp)
        cursor.execute(query, val)
        user_result = cursor.fetchall()

        

        if len(user_result) == 0:
            # ID / MDP Incorrect
            return render_template('index.html', connexionError=True)

        else:
            # ID et MDP Correct

            # Sélection des filières (copiée car la redirection est forcée pour le set_cookie)
            query = ("SELECT * FROM filiere")
            cursor.execute(query)
            filieres = cursor.fetchall()

            cnx.close()

            # Redirection forcée + ajout du cookie
            res = make_response(render_template("choixFiliere.html", filieres=filieres))
            res.set_cookie('compteConnecte', user_result[0][0], max_age=60*60*24)
            res.set_cookie('typeCompte', user_result[0][2], max_age=60*60*24) # Type de compte: "administrateur" ou "enseignant"
            return res
        
    # PAGE D'INDEX
    return render_template('index.html')


@app.route("/deconnexion", methods=["GET"])
def deconnexion():
    if 'compteConnecte' in request.cookies:
        #Vide le cookie
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

    

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()
    # Recuperation de la liste des filières
    query = ("SELECT * FROM filiere")
    cursor.execute(query)
    filieres = cursor.fetchall()

    cnx.close()

    #redirection vers la page qui affiche les filières disponibles
    return render_template("choixFiliere.html",filieres=filieres)


@app.route("/pageGenerale/<idFiliere>")
def pageGenerale(idFiliere):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Recuperation de tous les étudiants
    if idFiliere == "NULL":
        query = ("SELECT * FROM etudiant WHERE filiere IS NULL")
    else:
        query = ("SELECT * FROM etudiant WHERE filiere="+str(idFiliere))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    cursor.execute(query)
    etu = cursor.fetchall()

    # Filières (récupération du nom)
    if idFiliere == "NULL":
        filieres = [("NULL", "Étudiants sans filière")]
    else:
        query = ("SELECT * FROM filiere WHERE idfiliere="+str(idFiliere))
        cursor.execute(query)
        filieres = cursor.fetchall()


    # Présences étudiant
    query = ("SELECT * FROM presence") # Améliorer la durée de chargement ?
    cursor.execute(query)
    presence = cursor.fetchall()
    cnx.close()
    # Génération du excel a chaque fois qu'on est sur la page générale
    excelGen.creation()
    return render_template("pageGenerale.html",user=etu,presence=presence,filieres=filieres)

@app.route("/pageEtu/<id>")
@app.route("/pageEtu/<id>", methods=["GET", "POST"])
def pageEtu(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    id=id

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()
    
    modifType = 0   # Utilisé en cas de modifs utilisateur
                    # 0 = rien, 1 = succès, -1 = erreur
    msgErr = ""     # Utilisé en cas d'erreur (pour l'affichage)

    # si un formulaire à été envoyé à cette page
    if request.method == "POST":
        # recuperation des informations du formulaire
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
        
        val = (idCarteEtu,nom,prenom,numeroEtudiant,typeContratEtudiant,tarif,filiere,numeroTel,mailEtu,mailEntreprise,id)

        # Modification de la table étudiant avec les nouvelles informations 
        query = ("UPDATE etudiant SET idCarteEtu=%s,nom=%s,prenom=%s,numeroEtudiant=%s,typeContratEtudiant=%s,tarif=%s,filiere=%s,numeroTel=%s,mailEtu=%s,mailEntreprise=%s WHERE idCarteEtu=%s")

        try:
            cursor.execute(query,val)

            query = ("UPDATE presence SET idCarteEtu=%s WHERE idCarteEtu=%s")
            val = (idCarteEtu,id)

            cursor.execute(query,val)
            cnx.commit()

            modifType = 1
            
        except Exception as ex:
            cnx.rollback()
            modifType = -1
            msgErr = repr(ex)
            

    # recuperation des étudiants et de leurs présence
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()
    
    query = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    presence = cursor.fetchall()
    cnx.close()

    return render_template("pageEtu.html", user=etu , presence=presence, modifType=modifType, msgErreur=msgErr)

@app.route("/pageConvention/<id>", methods=["GET", "POST"])
def pageConvention(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    id=id

    #recuperation de l'étudiants concerné
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()
    cnx.close()


    if request.method == "POST":

        #Recuperation et sauvegarde du fichier transmis dans le dossier cenvention
        conv = request.files["conv"]
        non_conv = secure_filename(conv.filename)
        conv.save('/root/TeamRVBS/app/static/convention/'+non_conv)
    
    #pour savoir si l'étudiant possède déjà une convention
    p = "/root/TeamRVBS/app/static/convention/"+str(etu[0][1]) + "_" + str(etu[0][2])+"_Convention.pdf"
    if not(path.exists(p)):
        p = "../static/convention/conventionBase.pdf"
    else:
        p = "../static/convention/"+ str(etu[0][1]) + "_" + str(etu[0][2]) +"_Convention.pdf"
    return render_template("pageConvention.html",user=etu,path=p) 




@app.route("/pageModifEtu/<id>")
def pageModifEtu(id):

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    id=id

    #recuperation de létudiant et des filières
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    query = ("SELECT * FROM filiere")
    cursor.execute(query)
    filiere = cursor.fetchall()
    
    cnx.close()
    
    return render_template("pageModifEtu.html", user=etu, fil=filiere)

@app.route("/pdfEtuPresence/<id>")
def pdfEtuPresence(id): 
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    id=id
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    query = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][6]))
    cursor.execute(query)
    filiere = cursor.fetchall()

    query = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    presence = cursor.fetchall()

    query=("SELECT * FROM administration")
    cursor.execute(query)
    administration = cursor.fetchall()

    cnx.close()

    myPresence= pdfgen.presence(etu[0][1]+" "+etu[0][2],filiere[0][1],presence,administration)
    return render_template("pdfEtu.html",myPresence=myPresence,user=etu)

@app.route("/pdfEtu/<id>")
def pdfEtu(id): 

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    id=id 
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    query = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    presence = cursor.fetchall()

    query = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][6]))
    cursor.execute(query)
    filiere = cursor.fetchall()
    
    query=("SELECT * FROM administration")
    cursor.execute(query)
    administration = cursor.fetchall()

    cnx.close()


    myPDF=pdfgen.pdf(etu[0][1]+" "+etu[0][2],filiere[0][1],presence,administration)
    return render_template("pdfEtuAttest.html",myPDF=myPDF,user=etu)

@app.route("/archiveEtu/<id>")
@app.route("/archiveEtu/<id>", methods=["GET","POST"])
def archiveEtu(id):
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page étudiant
    if not compteEstAdmin():
        return redirect(url_for("pageEtu", id=id))

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()
    
    if request.method == 'POST':
        #si arrive ici avec formulaire alors il faut trouver l'id de l'étudiant
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        query = ("SELECT * FROM etudiant WHERE nom=%s AND prenom=%s")
        val = (nom,prenom)
        cursor.execute(query,val)
        rows = cursor.fetchall()
        #Il ne doit avoir récupérer qu'un étudiant
        for row in rows:
            id = row[0] #idCarteEtu

        #On regarde que l'id a bien était initialisé (si id = 0 l'étudiant n'est pas dans la bdd)
        if(int(id) == 0):
            return render_template("archive.html", aucunResultat=True, nomEtu=nom, prenomEtu=prenom)
            
    import re
    #On récupère les informations de l'étudiant 
    query = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    cnx.close()
    #Création de deux regex pour récupérer les fichiers attestation.pdf et presence.pdf de l'étudiant en question
    attestationRegex=rf".*{etu[0][1]}\s{etu[0][2]}\sAttestation\.pdf"
    presenceRegex=rf".*{etu[0][1]}\s{etu[0][2]}\sPresence\.pdf"

    #Récupération de la liste des fichiers de l'archive
    folderContent = os.listdir(os.path.join("./app/static/archive"))

    #Création de deux tableaux pour récupérer dans chacun deux les fichiers voulu
    fichiersAttestation = []
    fichierPresence = []

    for i in folderContent:
        #on passe tout les fichiers de l'archive dans les regex, quand ils correspondent on les ajoutes au tableau correspondant
        if (re.match(attestationRegex,i)!=None):
            fichiersAttestation.append(i)

        if(re.match(presenceRegex,i)!=None):
            fichierPresence.append(i)
            
    return render_template("archiveEtu.html",user=etu, folderAttestation=fichiersAttestation, folderFichePresence=fichierPresence) 


#Sert a ajouter un étudiant depuis l'application mobile
@app.route("/ajoutEtu/<nomprenomid>",methods=["GET","POST"])
def ajoutEtu(nomprenomid):
    np = str(nomprenomid).split('-')
    idCarte = int(np[2])
    nom = np[0]
    prenom = np[1]
    numEtu = np[3]

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #insertion de l'etudiant dans la BDD
    query = ("INSERT INTO etudiant (idCarteEtu,nom,prenom,numeroEtudiant) VALUES (%s,%s,%s,%s)")
    arg = (idCarte,nom,prenom,numEtu)
    try:
        cursor.execute(query,arg)
        cnx.commit()
        cnx.close()
        return render_template("success.html")
    except:
        cnx.rollback()
        cnx.close()
        return render_template("failure.html")

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

        data = request.form['tsa']
                
        if data:
            fonctionPy.sendDates(data)
        else:
            fonctionPy.effacerBase()

    dates = fonctionPy.recupererDates()
    

    return render_template("emploiDuTempsPicker.html",dates=dates)
    
@app.route("/pageAdministration")
def pageAdministration():
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")
 
    return render_template("pageAdministration.html")

@app.route("/adminModifVariable")
@app.route("/adminModifVariable", methods=["GET", "POST"])
def adminModifVariable():
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    modifType = 0   # Utilisé en cas de modifs utilisateur
                    # 0 = rien, 1 = succès, -1 = erreur
    msgErr = ""     # Utilisé en cas d'erreur (pour l'affichage)

    
    if request.method == "POST":
        #Récupération des valeurs du formulaire (cas ou on a cliqué sur valider depuis la page adminModifVariable.html)
        debutAnnee = request.form["debutAnnee"]
        finAnnee = request.form["finAnnee"]
        debutAffiche = request.form["debutPeriode"]
        finAffiche = request.form["finPeriode"]
        presidentSMB = request.form["presidentUSMB"]
        presidentSFC = request.form["presidentSFC"]
        tarifMaster = int(request.form["tarifMaster"])

        #On met a jour la bdd
        query = ("UPDATE administration SET debutAnnee=%s,finAnnee=%s,debutAffiche=%s,finAffiche=%s,presidentSMB=%s,presidentSFC=%s,tarfiMaster=%s")
        val = (debutAnnee,finAnnee,debutAffiche,finAffiche,presidentSMB,presidentSFC,tarifMaster)

        try:
            cursor.execute(query,val)
            cnx.commit()            
            modifType = 1     
        
        except Exception as ex:
            cnx.rollback()
            modifType = -1
            msgErr = repr(ex)
    
    #On récupère les informations de la bdd pour les affichers dans le formulaire
    query = ("SELECT * FROM administration ")
    cursor.execute(query)
    admin = cursor.fetchall()
    cnx.close()
    return render_template("adminModifVariable.html",admin=admin, modifType=modifType, msgErreur=msgErr)

@app.route("/creationCompte", methods=['GET', 'POST'])
def creationCompte():
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")

    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()
    
    modifType = 0   # Utilisé en cas de modification
                    # 0 = rien, 1 = succès, -1 = erreur
    idCompte = ""   # Utilisé en cas de modification
    msgErr = ""     # Utilisé en cas d'erreur (pour l'affichage)

    if request.method == "POST":
        #Recuperation des information du compte
        email = request.form["nomCompte"]
        mdp = mdpGen.generateurMDP() #generation du mot de passe
        typeCompte = request.form["type"]
        idCompte = email

        #Insertion du compte
        query = ("INSERT INTO connexion VALUES(%s,%s,%s)")
        val =(email,mdp,typeCompte)

        try:
            cursor.execute(query,val)
            cnx.commit()
            cnx.close()
            mdpGen.envoiMail(email,mdp) #evoi de l'email recapitulatif
            modifType = 1

        except Exception as ex:
            cnx.rollback()
            cnx.close()
            modifType = -1
            msgErr = repr(ex)
    cnx.close()
    return render_template("creationCompte.html", modifType=modifType, msgErreur=msgErr, identifiant=idCompte)

@app.route("/gestionCompte", methods=['GET', 'POST'])
def gestionCompte():
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")
    
    modifType = 0   # Utilisé en cas de modification
                    # 0 = rien, 1 = succès, -1 = erreur
    idCompte = ""   # Utilisé en cas de modification
    msgErr = ""     # Utilisé en cas d'erreur (pour l'affichage)
    
    if request.method == "POST":

        #recuperation des nouvelles informations
        nom = request.form["nomCompte"]
        mdp = request.form["mdp"]

        idCompte = nom

        cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
        cursor = cnx.cursor()

        # Vérifie que le compte existe
        query = ("SELECT * FROM connexion WHERE identifiant='"+nom+"'")
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            # Compte inexistant, erreur
            modifType = -1
            msgErr = "Le compte n'existe pas."

        else:
            # Le compte existe, mise à jour de la BDD
            query = ("UPDATE connexion SET motdepasse=%s WHERE identifiant=%s")
            val = (mdp,nom)
            try:
                cursor.execute(query,val)
                cnx.commit()
                cnx.close()
                mdpGen.envoiMailModif(nom,mdp) # envoi de l'email de modification
                modifType = 1
                
            except Exception as ex:
                cnx.rollback()
                cnx.close()
                modifType = -1
                msgErr = repr(ex)

    return render_template("gestionCompte.html", modifType=modifType, msgErreur=msgErr, identifiant=idCompte)

@app.route("/archive")
def archive():
    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")

    return render_template("archive.html", aucunResultat=False, nomEtu="", prenomEtu="")
