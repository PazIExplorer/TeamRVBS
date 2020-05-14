import mysql.connector, json, os
import datetime
import sqlite3
import time

from app.pythonScript import config

# On lui donne un étudiant a partir de son numéro de carte étudiant
# La fonction renvoie un tableau avec les heures de présences / mois 
#
def heurePresentParMois(numCarteEtu):
    #initialisation tab
    tab_presence = {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0}
    tab_des_mois = {"1":"Janv", "2":"Fev", "3":"Mars", "4":"Avril", "5":"Mai", "6":"Juin", "7":"Juil", "8":"Aout", "9": "Sept", "10":"Oct", "11":"Nov", "12":"Déc"}

    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #Récupération de la présence de l'étu
    query = ("SELECT matin, apresMidi, datePresence FROM presence WHERE numeroEtudiant="+str(numCarteEtu))
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        #pour chaque rows : récupérer la datePresence 
        dateCourant = row[2]
        #en récupérer le moi (ex : "09")
        numMois = recupMois(dateCourant)
        #récupérer le nom du mois ("Sept")
        nomMois = tab_des_mois[numMois]

        #ajouter +4 pour le matin et +3 pour l'aprem dans le tab_presence au bon mois
        if(row[0] == 1 or row[0] == 3):
            tab_presence[nomMois] = tab_presence[nomMois] + 4
        if(row[1] == 1 or row[1] == 3):
            tab_presence[nomMois] = tab_presence[nomMois] + 3
    return tab_presence

# On lui donne un étudiant a partir de son numéro de carte étudiant
# La fonction renvoie un tableau avec les heures de présences / mois
# dans la limite d'affichage pour les fiches / attestations de présence
#
def heurePresentParMoisLimiteAffichage(numCarteEtu):
    #initialisation tab
    tab_presence = {}
    tab_des_mois = {"1":"Janvier", "2":"Février", "3":"Mars", "4":"Avril", "5":"Mai", "6":"Juin", "7":"Juillet", "8":"Août", "9": "Septembre", "10":"Octobre", "11":"Novembre", "12":"Décembre"}

    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #Récupération de la présence de l'étu
    query = ("SELECT matin, apresMidi, datePresence FROM presence WHERE numeroEtudiant="+str(numCarteEtu))
    cursor.execute(query)
    rows = cursor.fetchall()

    # Dates d'affichage
    query = ("SELECT debutAffiche, finAffiche FROM administration")
    cursor.execute(query)
    admin = cursor.fetchall()
    debutAffiche = datetime.datetime.strptime(admin[0][0], '%d/%m/%Y')
    finAffiche = datetime.datetime.strptime(admin[0][1], '%d/%m/%Y') 
    
    # Création du tableau de mois
    moisDebut = debutAffiche.month
    anneeDebut = debutAffiche.year
    moisFin = finAffiche.month
    anneeFin = finAffiche.year

    if anneeDebut == anneeFin:
        for i in range(moisDebut, moisFin+1):
            mois = tab_des_mois[str(i)]
            if nomMois not in tab_presence:
                tab_presence[nomMois] = 0 # Mois non existent, on l'ajoute dans la liste
    else:
        for i in range(moisDebut, moisFin+1+12):
            nomMois = ""
            if i <= 12:
                nomMois = tab_des_mois[str(i)]
            elif i > 12 and i < moisDebut+12:
                nomMois = tab_des_mois[str(i-12)]
            
            if i < moisDebut+12 and nomMois not in tab_presence:
                tab_presence[nomMois] = 0 # Mois non existent, on l'ajoute dans la liste

    # Ajout des heures de présence le tableau
    for row in rows:
        #pour chaque rows : récupérer la datePresence 
        dateCourant = row[2]
        datetimeCourant = datetime.datetime.strptime(dateCourant, '%d/%m/%Y')

        #en récupérer le mois (ex : "09")
        numMois = recupMois(dateCourant)
        #récupérer le nom du mois ("Sept")
        nomMois = tab_des_mois[numMois]

        #ajouter +4 pour le matin et +3 pour l'aprem dans le tab_presence au bon mois
        if debutAffiche <= datetimeCourant and datetimeCourant <= finAffiche:
            if(row[0] == 1 or row[0] == 3):
                tab_presence[nomMois] = tab_presence[nomMois] + 4
            if(row[1] == 1 or row[1] == 3):
                tab_presence[nomMois] = tab_presence[nomMois] + 3
    
    return tab_presence

def recupMois(datePresence):
    liste = list(datePresence)
    i = 0
    flag = False
    chaine = ""
    while i < len(liste):
        if(flag == True):
            if(liste[i] == '/'):
                flag = False
            else:
                chaine = chaine+liste[i]

        else:
            if(liste[i] == '/'):
                flag = True

        i = i+1
    return chaine


#Récupérer les dates de la bdd
def recupererEmploiDuTemps():
    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #récupérer les jours de cours de la bdd
    query = ("SELECT *, DATE_FORMAT(jourDeCour, \"%m/%d/%Y\") FROM calendrier")
    cursor.execute(query)
    rows = cursor.fetchall()

    #Met les données dans la list python
    liste_jours = []
    for row in rows:
        liste_jours.append(row[1]) #row[0] la date sql avec le format de base, row[1] avec format %m/%d/%

    #Ouvre le fichier emploiDuTempse.json en écriture et écrit la liste des jours de cours dedans 
    with open("app/static/json/emploiDuTempsPick.json", "w") as file:
        json.dump(liste_jours, file)

#But : convertir une date qui est dans une chaine de caractères de format mm/jj/aaaa en une datetime.date
def dateStringToDatetime(dateEnString):

    annee = dateEnString[6]+dateEnString[7]+dateEnString[8]+dateEnString[9]
    mois = dateEnString[0]+dateEnString[1]
    jour = dateEnString[3]+dateEnString[4]

    myDate = datetime.datetime(int(annee), int(mois), int(jour), 0, 0, 0)
    return myDate


def sendEmploiDuTemps(jsonDates):
    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #récupération de la liste des jours a partir du json
    liste_jours = json.loads(jsonDates)
    
    #vide la table 
    query = ("TRUNCATE TABLE calendrier")
    cursor.execute(query)

    #parcour de la liste pour les envoyer dans la bdd

    for i in range (0, len(liste_jours)):
        #Convertion de la date du json qui est en string en format datetime
        dateCourante = dateStringToDatetime(list(liste_jours[i]))
        query = ('INSERT INTO calendrier (jourDeCour) values(%s)')
        var = (dateCourante.strftime('%Y-%m-%d %H:%M:%S'),)
        cursor.execute(query, var)

    cnx.commit()
   # except: 
    #    cnx.rollback()
    
    #cnx.close()

def tabHeureCoursParMois(anneeScolaireDebut, anneeScolaireFin):
    #initialisation tab
    tab_heureCourParMois = {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0}
    tab_des_mois = {"01":"Janv", "02":"Fev", "03":"Mars", "04":"Avril", "05":"Mai", "06":"Juin", "07":"Juil", "08":"Aout", "09": "Sept", "10":"Oct", "11":"Nov", "12":"Déc"}

    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #Récupération des jours ou les étudiants doivent être présent
    query = ("SELECT *, DATE_FORMAT(jourDeCour, \"%m/%d/%Y\") FROM calendrier")
    cursor.execute(query)
    rows = cursor.fetchall()

    #row[0] la date sql avec le format de base, row[1] avec format %m
    for row in rows:
        jourCourant = row[1]
        num_mois = jourCourant[0]+jourCourant[1] 
        annee = jourCourant[6]+jourCourant[7]+jourCourant[8]+jourCourant[9]

        if(int(annee) == int(anneeScolaireDebut) or int(annee) == int(anneeScolaireFin)):
            nom_mois = tab_des_mois[num_mois]
            tab_heureCourParMois[nom_mois] = tab_heureCourParMois[nom_mois] + 7 #on ajoute 7h (le nb d'heure de cours dans une journée)
    return tab_heureCourParMois



#Récupérer les dates de la bdd
def recupererDates():
    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #récupérer les jours de cours de la bdd
    query = ("SELECT *, DATE_FORMAT(jourDeCour, \"%Y-%m-%d\") FROM calendrier")
    cursor.execute(query)
    rows = cursor.fetchall()
    cnx.close()

    dates = []
    if len(rows) != 0:
        for e in rows:
            dates.append(e[1])

    return dates



def sendDates(Dates):
    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    #récupération de la liste des jours a partir du json
    if Dates == '':
        return 0
    else:
        liste_jours = []
        liste_jours = Dates.split('/')

    
    #vide la table 
    query = ("DELETE FROM calendrier")
    cursor.execute(query)

    #parcour de la liste pour les envoyer dans la bdd
    
    for i in range (0, len(liste_jours)-1):
        
        dateCourante = time.strptime(str(liste_jours[i]),"%Y-%m-%d")
        query = ('INSERT INTO calendrier (jourDeCour) VALUES (%s)')
        var = (time.strftime('%Y-%m-%d', dateCourante),)
        cursor.execute(query, var)

        cnx.commit()

    
    cnx.close()


def effacerBase():
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    query = ("DELETE FROM calendrier")
    cursor.execute(query)

    cnx.commit()

    cnx.close()