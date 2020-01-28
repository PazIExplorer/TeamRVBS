from app import app
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
    return render_template("pageGenerale.html")

@app.route("/pageEtu")
def pageEtu():
    return render_template("pageEtu.html")
