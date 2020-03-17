from app import app
#from app import db
#from app.models import Filiere, Etudiant, Presence
from flask import render_template, request
from werkzeug import secure_filename
import mysql.connector

import os
from app.pythonScript import pdfgen



cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
cursor = cnx.cursor()
cursora = cnx.cursor()
cursorb = cnx.cursor()
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_mdp = request.form["user_mdp"]
        
        #----------------
        # Voir la connexion a partir de la bdd
        #--------------------
        if user_name == "Admin" and user_mdp == "Admin":
            return render_template("choixFiliere.html")
        
    return render_template('index.html')

@app.route("/choixFiliere")
def choixFiliere():
    return render_template("choixFiliere.html")

@app.route("/pageGenerale")
def pageGenerale():
    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    etu = cursor.fetchall()
    for e in etu:
        print(str(e[0]))



    query = ("SELECT * FROM presence")
    cursor.execute(query)
    presence = cursor.fetchall()
    
    return render_template("pageGenerale.html",user=etu,presence=presence)


@app.route("/pageEtu/<id>", methods=["GET", "POST"])
def pageEtu(id):
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
    id=id
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()
    #etu[0][0]= hex(etu[0][0])
    return render_template("pageModifEtu.html", user=etu)

@app.route("/pdfEtuPresence/<id>")
def pdfEtuPresence(id): 
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


