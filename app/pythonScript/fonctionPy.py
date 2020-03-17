import mysql.connector


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
    query = ("SELECT matin, apresMidi, datePresence FROM presence WHERE idCarteEtu = "+str(numCarteEtu))
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        #pour chaque rows : récupérer la datePresence 
        dateCourant = row[2]
        #en récupérer le moi (ex : "09")
        numMoi = recupMoi(dateCourant)
        #récupérer le nom du moi ("Sept")
        nomMoi = tab_des_mois[numMoi]
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