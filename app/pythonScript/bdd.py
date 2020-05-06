import mysql.connector

def requete(cnx,cursor):
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    return (cnx,cursor)

def finRequete(cnx):
    cnx.close
    return cnx