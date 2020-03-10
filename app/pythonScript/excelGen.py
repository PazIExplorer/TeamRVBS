import xlwt
import mysql.connector
import sqlite3

def creation():
    wb = xlwt.Workbook() #création d'un classeur
    ws = wb.add_sheet("Ma feuille") #création d'une feuille

    row, col = 1, 2
    ws.write(row, col, "Année scolaire a mettre")



    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()
    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    rows = cursor.fetchall()
    #affichage n°, nom, prenom
    row = 8
    col = 0
    i = 1
    for etu in rows:
        ws.write(row+i, col, i)
        ws.write(row+i, col+1, etu[1]+" "+etu[2])
        i = i+1

    
    wb.save('app/static/excel/output.xls')

    return 0