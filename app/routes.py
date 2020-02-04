from app import app
from app import db
from app.models import Filiere, Etudiant, Presence
from flask import render_template, request

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
    etu = Etudiant.query.all()
    return render_template("pageGenerale.html",user=etu)

@app.route("/pageEtu/<id>")
def pageEtu(id):
    id=id
    etu = Etudiant.query.get(int(id))
    #presence ='TEST'
    
    presence = Presence.query.filter_by(idCarteEtu=int(id)).all()
    #print(presence[0].date)
    return render_template("pageEtu.html", user=etu , presence=presence)


