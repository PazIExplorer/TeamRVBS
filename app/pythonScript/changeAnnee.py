import mysql.connector
import shutil #pour la copie de fichier
import os

from app.pythonScript import config
from app.pythonScript import pdfgen
from app.pythonScript import excelGen



def changeTableAdmin(dateD,dateF):
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    query = ("UPDATE administration SET debutAnnee=%s,finAnnee=%s,debutAffiche=%s,finAffiche=%s")
    val = (dateD,dateF,dateD,dateF)

    try:
        cursor.execute(query,val)          
        cnx.commit()
        cnx.close()
        return 1
    except:
        cnx.rollback()
        cnx.close()
        return -1

def genereFeuilles(anneeP,anneeF):
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()


    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    etu = cursor.fetchall()

    query=("SELECT * FROM administration")
    cursor.execute(query)
    administration = cursor.fetchall()

    query = ("SELECT * FROM filiere")
    cursor.execute(query)
    filiere = cursor.fetchall()

    for f in filiere:
        if int(f[0]) != 100:
            excelGen.creation(f[0])
            shutil.copy(os.getcwd()+"/app/static/excel/forfaitHorraire.xlsx",os.getcwd()+"/app/static/excel/forfaitHorraire_global_"+ str(anneeP) + "-" + str(anneeF) + "_" + str(f[1]) + ".xlsx")
            #print(os.getcwd())

    for e in etu:
        query = ("SELECT * FROM presence WHERE numeroEtudiant="+str(e[3]))
        cursor.execute(query)
        presence = cursor.fetchall()
        
        if str(e[6]) != 'None' or int(e[6]) != 100:
            query = ("SELECT * FROM filiere WHERE idFiliere="+str(e[6]))
            cursor.execute(query)
            filiere = cursor.fetchall()
            
            #génération des attestations globales
            pdfgen.pdf(e[1]+" "+e[2],filiere[0][1],presence,administration)

            #Génération des fiches de présences globales
            pdfgen.presence(e[1]+" "+e[2],filiere[0][1],presence,administration)

    cnx.close()

def nettoyageBDD():
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #Remise à zero du calnedrier alternant
    query = ("DELETE FROM calendrier")
    cursor.execute(query)
    cnx.commit()

    #Remise à zéro des présences
    #query = ("DELETE FROM presence")
    #cursor.execute(query)
    #cnx.commit()

    #déplacement des étudiants dans la catégorie 'plus etudiant'
            # Modification de la table étudiant avec les nouvelles informations 
    query = ("UPDATE etudiant SET filiere=100")

    try:
        cursor.execute(query)
        cnx.commit()
        cnx.close()
        return 1
            
    except:
        cnx.rollback()
        cnx.close()
        return -1
        