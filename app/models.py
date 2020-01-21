from app import db

# Etudiant
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True)
    prenom = db.Column(db.String(64), index=True)
    idCarte = db.Column(db.String(64))

    def __repr__(self):
        return '<Etudiant {} {}>'.format(self.prenom, self.nom)

