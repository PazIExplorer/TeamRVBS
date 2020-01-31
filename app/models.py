from app import db
from datetime import datetime


#Filiere
class Filiere(db.Model):
    idFiliere = db.Column(db.Integer, primary_key=True)
    nomFiliere = db.Column(db.String(64))

    def __repr__(self):
        return '<Filiere {}>'.format(self.nomFiliere)


# Etudiant
class Etudiant(db.Model):
    idCarteEtu = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True)
    prenom = db.Column(db.String(64), index=True)
    numeroEtudiant = db.Column(db.Integer, index=True, unique=True)
    typeContratEtudiant = db.Column(db.String(64))
    tarif = db.Column(db.Integer)
    filiere = db.Column(db.Integer, db.ForeignKey('filiere.idFiliere'))
    numeroTel = db.Column(db.Integer)
    mailEtu = db.Column(db.String(64))
    mailEntreprise = db.Column(db.String(64))


    def __repr__(self):
        return '<Etudiant {} {}>'.format(self.prenom, self.nom)

#Presence
class Presence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matin = db.Column(db.String(64))
    apresMidi = db.Column(db.String(64))
    idCarteEtu = db.Column(db.Integer, db.ForeignKey('etudiant.idCarteEtu'))
    date = db.Column(db.String(64))

    def __repr__(self):
        return '<Presence {} {} {} {}>'.format(self.id, self.matin, self.apresMidi, self.date)
