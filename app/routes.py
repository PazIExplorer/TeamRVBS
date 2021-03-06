# -*-coding:utf-8 -*

from app import app
from flask import render_template, request, make_response, redirect, url_for
from werkzeug import secure_filename
import mysql.connector

import os.path
from os import path

from operator import itemgetter

import os
import re
import string

from app.pythonScript import pdfgen
from app.pythonScript import excelGen
from app.pythonScript import fonctionPy
from app.pythonScript import mdpGen
from app.pythonScript import changeAnnee

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
    query = ("SELECT * FROM filiere ORDER BY nomFiliere")
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

    # Tri des élèves par nom / prénom
    etu = sorted(etu, key=itemgetter(1,2))   # Tri par nom puis par prénom

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
    excelGen.creation(idFiliere)
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
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        numeroEtudiant = request.form["numeroEtudiant"]
        numeroBadge = request.form["numeroBadge"]
        typeContratEtudiant = request.form["typeContratEtudiant"]
        filiere = int(request.form["filiere"])
        numeroTel = request.form["numeroTel"]
        mailEtu = request.form["mailEtu"]
        mailEntreprise = request.form["mailEntreprise"]
        commentaire = request.form["commentaire"]



        #Vérification du formulaire :
        #Pour le nom de l'étudiant 
        if len(nom.strip()) == 0:
            modifType = -1
            msgErr = "Nom de l'étudiant invalide"
        #Pour le prénom de l'étudiant
        if len(prenom.strip()) == 0:
            modifType = -1
            msgErr = "Prenom de l'étudiant invalide"
        #Pour le numéro de la carte étudiante
        if len(numeroEtudiant.strip()) == 0:
            modifType = -1
            msgErr = "Numéro de carte étudiante invalide"
        #Pour le numéro de badgage
        if len(numeroBadge.strip()) == 0:
            modifType = -1
            msgErr = "Numéro de badge invalide"
        #Pour le tarif Vérif que c'est int

        #Pour le numéro de tel, pas important
        #Pour mail Etudiant, pas important
        #Pour mail Entreprise, pas important
        #Commentaire, pas important
        #Pour le numéro de tel
        if len(numeroTel.strip()) == 0:
            numeroTel = "non renseigné"

        #Pour mail Etudiant
        if len(mailEtu.strip()) == 0:
            mailEtu = "non renseigné"

        #Pour mail Entreprise, pas important
        if len(mailEntreprise.strip()) == 0:
            mailEntreprise = "non renseigné"

        #Commentaire, pas important
        if len(commentaire.strip()) == 0:
            commentaire = "non renseigné"


        if modifType != -1:
            numeroBadge = int(numeroBadge,16)
            val = (numeroBadge,nom,prenom,numeroEtudiant,typeContratEtudiant,filiere,numeroTel,mailEtu,mailEntreprise,commentaire,id)

            # Modification de la table étudiant avec les nouvelles informations 
            query = ("UPDATE etudiant SET idCarteEtu=%s,nom=%s,prenom=%s,numeroEtudiant=%s,typeContratEtudiant=%s,filiere=%s,numeroTel=%s,mailEtu=%s,mailEntreprise=%s,description=%s WHERE numeroEtudiant=%s")

            try:
                cursor.execute(query,val)
                cnx.commit()
                modifType = 1
            
            except Exception as ex:
                cnx.rollback()
                modifType = -1
                msgErr = repr(ex)
            
    # recuperation des étudiants et de leurs présence
    query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()
    
    query = ("SELECT * FROM presence WHERE numeroEtudiant="+str(id))
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
    query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()
    cnx.close()

    modifType=0
    msgErreur=''


    if request.method == "POST":

        #Recuperation et sauvegarde du fichier transmis dans le dossier cenvention
        conv = request.files["conv"]
        nom_conv = secure_filename(conv.filename)
        nom = str(etu[0][1]) + "_" + str(etu[0][2]) +"_Convention.pdf"
        if nom_conv == nom :
            conv.save(os.getcwd()+'/app/static/convention/'+nom_conv)
            modifType=1
        else :
            modifType=-1
            msgErreur = "Le fichier convention n'est pas au bon format (format accepté : \"Nom Prenom Convention.pdf\""

    
    #pour savoir si l'étudiant possède déjà une convention
    p = os.getcwd()+"/app/static/convention/"+str(etu[0][1]) + "_" + str(etu[0][2])+"_Convention.pdf"
    if not(path.exists(p)):
        p = "../static/convention/conventionBase.pdf"
    else:
        p = "../static/convention/"+ str(etu[0][1]) + "_" + str(etu[0][2]) +"_Convention.pdf"
    return render_template("pageConvention.html",user=etu,path=p,modifType=modifType,msgErreur=msgErreur) 




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
    query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
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
    query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    query = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][5]))
    cursor.execute(query)
    filiere = cursor.fetchall()

    query = ("SELECT * FROM presence WHERE numeroEtudiant="+str(id))
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
    query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
    cursor.execute(query)
    etu = cursor.fetchall()

    query = ("SELECT * FROM presence WHERE numeroEtudiant="+str(id))
    cursor.execute(query)
    presence = cursor.fetchall()

    query = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][5]))
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
    
    #Si on arrive depuis l'archive globale on récupère le nom et prénom du formulaire
    if request.method == 'POST':
        nom = request.form["nom"]
        prenom = request.form["prenom"]

    #Si on arrive depuis la page étudiant, a partir de l'id on récupère le nom et prénom de la bdd
    else :
        cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
        cursor = cnx.cursor()
        query = ("SELECT * FROM etudiant WHERE numeroEtudiant="+str(id))
        cursor.execute(query)
        etu = cursor.fetchall()
        cnx.close()
        nom = etu[0][1]
        prenom = etu[0][2]

    #Pour être sur que nom et prénom commence par une majuscule
    nom = nom.capitalize()
    prenom = prenom.capitalize()

    #Création de deux regex pour récupérer les fichiers attestation.pdf et presence.pdf de l'étudiant en question
    attestationRegex=rf".*{nom}\s{prenom}\s.*Attestation.*\.pdf"
    presenceRegex=rf".*{nom}\s{prenom}\s.*Feuille.*\.pdf"

    #Récupération de la liste des fichiers de l'archive
    folderContent = os.listdir(os.path.join("./app/static/archive"))

    #Création de deux tableaux pour récupérer dans chacun deux les fichiers voulu
    fichiersAttestation = []
    fichiersPresence = []

    for i in folderContent:
        #on passe tout les fichiers de l'archive dans les regex, quand ils correspondent on les ajoutes au tableau correspondant
        if (re.match(attestationRegex,i)!=None):
            fichiersAttestation.append(i)

        if(re.match(presenceRegex,i)!=None):
            fichiersPresence.append(i)
    
    # Tri des fichiers par nom
    fichiersAttestation.sort()
    fichiersPresence.sort()
    
    #Pour pouvoir afficher le nom et prénom de l'étudiant sur la page d'archive
    etu = (nom, prenom)
    return render_template("archiveEtu.html",user=etu, folderAttestation=fichiersAttestation, folderFichePresence=fichiersPresence) 


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
    query = ("INSERT INTO etudiant VALUES (%s,%s,%s,%s,'non renseigné','non renseigné','non renseigné','non renseigné','non renseigné','non renseigné')")
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
    modifType = 0

    # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")

    if request.method == 'POST':

        data = request.form['tsa']
                
        if data:
            err = fonctionPy.sendDates(data)
        else:
            err = fonctionPy.effacerBase()
        
        if err == 0:
            modifType=1
        else:
            modiType=-1

    dates = fonctionPy.recupererDates()

    return render_template("emploiDuTempsPicker.html",dates=dates, modifType=modifType)
    
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
        signature = request.files["signature"]

        

        query = ("UPDATE administration SET debutAnnee=%s,finAnnee=%s,debutAffiche=%s,finAffiche=%s,presidentSMB=%s,presidentSFC=%s,tarifMaster=%s")
        val = (debutAnnee,finAnnee,debutAffiche,finAffiche,presidentSMB,presidentSFC,tarifMaster)

        try:
            cursor.execute(query,val)
                       
            modifType = 1 
            if signature.filename != "":
                nom_fichier = secure_filename(signature.filename)
                if nom_fichier == "signature.png":
                    signature.save(os.getcwd()+'/app/static/img/'+nom_fichier)
                else :
                    cnx.rollback()
                    modifType = -1
                    msgErr = "Le fichier signature n'est pas au bon format (format accepté : \"signature.png\""    
            cnx.commit() 
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

        query = ("SELECT * FROM connexion")
        cursor.execute(query)
        comptes = cursor.fetchall()

        estCompte = False
        for c in comptes:
            if(nom == c[0]):
                estCompte = True
        
        if estCompte:
            #mise à jour de la BDD
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
        else:
            modifType = -1
            msgErr = "Ce compte n'existe pas"

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


@app.route("/documentation")
def documentation():

    return render_template("documentation.html")

@app.route("/changementAnnee",  methods=['GET', 'POST'])
def changementAnnee():

        # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")
    modifType = 0

    if request.method == "POST":
        dateDebutP = request.form["debutAnneeP"]
        dateFinP = request.form["finAnneeP"]

        dateDebut = request.form["debutAnnee"]
        dateFin = request.form["finAnnee"]

        anneeD = dateDebutP[6:11]
        anneeF = dateFinP[6:11]

        #Changement de la période des attestations pour qu'elles soient globales
        modifType = changeAnnee.changeTableAdmin(dateDebutP,dateFinP)
        
        #génération attestations/fiches/facturation
        changeAnnee.genereFeuilles(anneeD,anneeF)

        #Changements BDD
        changeAnnee.nettoyageBDD()

        #changement des dates pour celle de la nouvelle annee
        modifType = changeAnnee.changeTableAdmin(dateDebut,dateFin)

    return render_template("changementAnnee.html",modifType=modifType)

@app.route("/archiveT")
def archiveT():

    excel = os.listdir(os.path.join("./app/static/excel"))
    regex=rf"^forfaitHoraire_global.*\.xlsx$"

    #tableaux pour récupérer les fichiers souhaités
    file = []

    #traitement par nom de fichier correspondant avec la regex
    for e in excel:
        if (re.match(regex,e)!=None):
            file.append(e)
        print(e)
    file.sort()

    return render_template("archiveT.html", file=file)


@app.route("/ajouterFiliere",  methods=['GET', 'POST'])
def ajouterFiliere():
        # Validation du compte dans le cookie
    if not cookieEstValide():
        return redirect("index")

    # Vérifie si le compte est admin, sinon retour à la page d'accueil
    if not compteEstAdmin():
        return redirect("choixFiliere")
    modifType = 0
    msgErr = ""


    if request.method == "POST":
        cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
        cursor = cnx.cursor()

        query = ("SELECT * FROM filiere")
        cursor.execute(query)
        filiere = cursor.fetchall()

        nomFiliere = request.form["nomFiliere"]

        try:
            idF = len(filiere)
            if idF<100:
                query = ("INSERT INTO filiere VALUES (%s,%s)")
                val =(idF,nomFiliere)
                cursor.execute(query,val)
                cnx.commit()
                modifType = 1
            else:
                modifType = -1
                msgErr = "Nombre maximal de filière atteint" 
        except:
            cnx.rollback()
            modifType = -1

        cnx.close()
    

    return render_template("ajouterFiliere.html", modifType=modifType ,msgErr=msgErr)