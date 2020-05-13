import mysql.connector, json, os
import datetime
import sqlite3
import time

# On lui donne un étudiant a partir de son numéro de carte étudiant
# La fonction renvoie un tableau avec les heures de présences / moi 
#
def heurePresentParMoi(numCarteEtu):
    #initialisation tab
    tab_presence = {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0}
    tab_des_mois = {"1":"Janv", "2":"Fev", "3":"Mars", "4":"Avril", "5":"Mai", "6":"Juin", "7":"Juil", "8":"Aout", "9": "Sept", "10":"Oct", "11":"Nov", "12":"Déc"}

    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    #Récupération de la présence de l'étu
    query = ("SELECT matin, apresMidi, datePresence FROM presence WHERE numeroEtudiant="+str(numCarteEtu))
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        #pour chaque rows : récupérer la datePresence 
        dateCourant = row[2]
        #en récupérer le moi (ex : "09")
        numMoi = recupMoi(dateCourant)
        #récupérer le nom du moi ("Sept")
        nomMoi = tab_des_mois[numMoi]

        print(dateCourant)
        print(numMoi)
        print(nomMoi)
        #ajouter +4 pour le matin et +3 pour l'aprem dans le tab_presence au bon mois
        if(row[0] == 1 or row[0] == 3):
            tab_presence[nomMoi] = tab_presence[nomMoi] + 4
        if(row[1] == 1 or row[1] == 3):
            tab_presence[nomMoi] = tab_presence[nomMoi] + 3
    return tab_presence

def recupMoi(datePresence):
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
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    #récupérer les jours de cours de la bdd
    query = ("SELECT *, DATE_FORMAT(jourDeCour, \"%m/%d/%Y\") FROM calendrier")
    cursor.execute(query)
    rows = cursor.fetchall()

    #Met les données dans la list python
    liste_jours = []
    for row in rows:
        liste_jours.append(row[1]) #row[0] la date sql avec le format de base, row[1] avec format %m/%d/%Y

    #[DEBUG] afficher les jours récupérés de la bdd
    #print("\n\n-----------test print j de la bdd recup----------")
    #for t in liste_jours:
    #    print(t)


    #Ouvre le fichier emploiDuTempse.json en écriture et écrit la liste des jours de cours dedans 
    with open("app/static/json/emploiDuTempsPick.json", "w") as file:
        json.dump(liste_jours, file)

#But : convertir une date qui est dans une chaine de caractères de format mm/jj/aaaa en une datetime.date
def dateStringToDatetime(dateEnString):

    annee = dateEnString[6]+dateEnString[7]+dateEnString[8]+dateEnString[9]
    moi = dateEnString[0]+dateEnString[1]
    jour = dateEnString[3]+dateEnString[4]

    myDate = datetime.datetime(int(annee), int(moi), int(jour), 0, 0, 0)
    return myDate


def sendEmploiDuTemps(jsonDates):
    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
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
       #print(dateCourante.year, dateCourante.month, dateCourante.day)
        query = ('INSERT INTO calendrier (jourDeCour) values(%s)')
        var = (dateCourante.strftime('%Y-%m-%d %H:%M:%S'),)
        cursor.execute(query, var)

    cnx.commit()
   # except: 
    #    cnx.rollback()
     #   print("DEBUG : fonction.py sendEmploiDutemps problème lors de l'insert a la bdd")
    
    #cnx.close()

def tabHeureCoursParMoi(anneeScolaireDebut, anneeScolaireFin):
    #initialisation tab
    tab_heureCourParMoi = {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0}
    tab_des_mois = {"01":"Janv", "02":"Fev", "03":"Mars", "04":"Avril", "05":"Mai", "06":"Juin", "07":"Juil", "08":"Aout", "09": "Sept", "10":"Oct", "11":"Nov", "12":"Déc"}

    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    #Récupération des jours ou les étudiants doivent être présent
    query = ("SELECT *, DATE_FORMAT(jourDeCour, \"%m/%d/%Y\") FROM calendrier")
    cursor.execute(query)
    rows = cursor.fetchall()

    #row[0] la date sql avec le format de base, row[1] avec format %m
    for row in rows:
        jourCourant = row[1]
        num_moi = jourCourant[0]+jourCourant[1] 
        annee = jourCourant[6]+jourCourant[7]+jourCourant[8]+jourCourant[9]

        if(int(annee) == int(anneeScolaireDebut) or int(annee) == int(anneeScolaireFin)):
            nom_moi = tab_des_mois[num_moi]
            tab_heureCourParMoi[nom_moi] = tab_heureCourParMoi[nom_moi] + 7 #on ajoute 7h (le nb d'heure de cours dans une journée)
    return tab_heureCourParMoi



#Récupérer les dates de la bdd
def recupererDates():
    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
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
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
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
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    query = ("DELETE FROM calendrier")
    cursor.execute(query)

    cnx.commit()

    cnx.close()