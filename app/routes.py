from app import app
#from app import db
#from app.models import Filiere, Etudiant, Presence
from flask import render_template, request
from werkzeug import secure_filename
import mysql.connector

import os
print(os.path.join(os.getcwd(),"app/","pdfgen.py"))
print(os.path.isfile(os.path.join(os.getcwd(),"app/","pdfgen.py")))
from app import pdfgen



cnx = mysql.connector.connect(host='localhost',database='badgeuse',user='ben',password='teamRVBS')
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

    query = ("SELECT * FROM presence")
    cursor.execute(query)
    presence = cursor.fetchall()
    #etu = Etudiant.query.all()
    #presence = Presence.query.all()

    return render_template("pageGenerale.html",user=etu,presence=presence)

@app.route("/pageEtu/<id>", methods=["GET", "POST"])
def pageEtu(id):
    id=id
    if request.method == "POST":
        idCarteEtu = int(request.form["idCarteEtu"])
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        numeroEtudiant = int(request.form["numeroEtudiant"])
        typeContratEtudiant = request.form["typeContratEtudiant"]
        tarif = float(request.form["tarif"])
        filiere = int(request.form["filiere"])
        numeroTel = int(request.form["numeroTel"])
        mailEtu = request.form["mailEtu"]
        mailEntreprise = request.form["mailEntreprise"]	
        print(nom)
        print(prenom)
        querya = ("UPDATE etudiant SET idCarteEtu=%s,nom=%s,prenom=%s,numeroEtudiant=%s,typeContratEtudiant=%s,tarif=%s,filiere=%s,numeroTel=%s,mailEtu=%s,mailEntreprise=%s WHERE idCarteEtu=%s")
        val = (idCarteEtu,nom,prenom,numeroEtudiant,typeContratEtudiant,tarif,filiere,numeroTel,mailEtu,mailEntreprise,id)
        #querya = ("UPDATE etudiant SET nom = %s WHERE idCarteEtu=%s")
        #val = (nom,id)
        try:
            cursora.execute(querya,val)
            cnx.commit()
            querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
            cursora.execute(querya)
            etu = cursora.fetchall()
            for e in etu:
                print(e[1])

            print("try")
        except:
            print("except")
            cnx.rollback()
    
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()
    #for e in etu:
        #print(e[1])
    #etu = Etudiant.query.get(int(id))
    #presence ='TEST'
    
    queryb = ("SELECT * FROM presence WHERE idCarteEtu="+str(id))
    cursorb.execute(queryb)
    presence = cursorb.fetchall()
    #for p in presence:
        #print(p[1])
    #presence = Presence.query.filter_by(idCarteEtu=int(id)).all()
    #print(presence[0].date)
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

    return render_template("pageModifEtu.html", user=etu)


@app.route("/pdfEtu/<id>")
def pdfEtu(id): 
    id=id 
    querya = ("SELECT * FROM etudiant WHERE idCarteEtu="+str(id))
    cursora.execute(querya)
    etu = cursora.fetchall()

    querya = ("SELECT * FROM filiere WHERE idFiliere="+str(etu[0][6]))
    cursora.execute(querya)
    filiere = cursora.fetchall()
    #etu= Etudiant.query.get(int(id))
    #filiere=Filiere.query.get(int(etu.filiere))
    myPDF=pdfgen.pdf(etu[
0][1]+" "+etu[0][2],filiere[0][1])
    return render_template("pdfEtu.html",myPDF=myPDF,user=etu)

@app.route("/pdfEtu/<id>")
def pdfEtu(id): 
    id=id 
    etu= Etudiant.query.get(int(id))
    filiere=Filiere.query.get(int(etu.filiere))
    myPDF=pdfgen.pdf(etu.nom+" "+etu.prenom,filiere.nomFiliere)
    return render_template("pdfEtu.html",myPDF=myPDF,user=etu)
