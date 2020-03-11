import mysql.connector


# On lui donne un étudiant a partir de son numéro de carte étudiant
# La fonction renvoie un tableau avec les heures de présences / moi 
#
def heurePresentParMoi(numCarteEtu):
    #initialisation tab
    tab_presence = {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0}
    tab_des_mois = {"01":"Janv", "02":"Fev", "03":"Mars", "04":"Avril", "05":"Mai", "06":"Juin", "07":"Juil", "08":"Aout", "09": "Sept", "10":"Oct", "11":"Nov", "12":"Déc"}

    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    #Récupération de la présence de l'étu
    query = ("SELECT matin, apresMidi, datePresence FROM presence WHERE etudiant_idx = "+numCarteEtu)
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        a = 2
        #pour chaque rows : récupérer la datePresence 
        #en récupérer le moi (ex : "09")
        #récupérer le nom du moi ("Sept") 
        #ajouter +4 pour le matin et +3 pour l'aprem dans le tab_presence au bon mois

    return tab_presence