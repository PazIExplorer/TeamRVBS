import xlsxwriter
import mysql.connector
import sqlite3

def creation():
    #VALEUR A MODIFIER
    dateDebut = 2019
    dateFin = 2020
    tarifConv = '8 500,00€'

    #connection bdd
    cnx = mysql.connector.connect(host='192.168.176.21',database='badgeuse',user='ben',password='teamRVBS')
    cursor = cnx.cursor()

    #Création du fichier et de la feuille
    wb = xlsxwriter.Workbook('app/static/excel/out.xlsx') #création d'un classeur
    ws = wb.add_worksheet()

    #Déclaration des formats
    formatBasic = wb.add_format({'border':1})
    

    formatCp = wb.add_format() #Format pour CP
    formatCp.set_border(1)
    formatCp.set_align('center')
    formatCp.set_bg_color('blue')

    formatCa = wb.add_format() #Format pour CA
    formatCa.set_border(1)
    formatCa.set_align('center')
    formatCa.set_font_color('red')

    wrap = wb.add_format({'text_wrap': True})
    #ws.set_column('A8:U15', 'T', format1)

    #Créations de l'en-tête 
    ws.merge_range('B3:J3', 'RECAPITULATIF DES HEURES SUIVIES PAR STAGIARES EN M2 ISC _ 400 HEURES')
    row, col = 0, 1
    ws.write('B1:B1', "SFC ...")

    #Dimension des colonnes
    ws.set_column('A:A', 2)
    ws.set_column('B:B', 40)

    #Récupération des étudiants de la base
    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    rows = cursor.fetchall()

    #affichage des titres du tableau
    ws.merge_range('C6:C7', 'CP/CA')
    ws.merge_range('D6:D7', 'TARIF\nCONV.', wrap)
    ws.write('E6:E6', 'Sept')
    ws.write('E7:E7', '???')
    ws.write('F6:F6', 'Oct')
    ws.write('F7:F7', '???')
    ws.write('G6:G6', 'Nov')
    ws.write('G7:G7', '???')
    ws.write('H6:H6', 'Déc')
    ws.write('H7:H7', '???')
    ws.write('I6:I6', str(dateDebut)+' T1')
    ws.write('I7:I7', '???')
    ws.merge_range('J6:J7', 'FACTURATION\nT1', wrap)
    ws.write('K6:K6', 'Janv')
    ws.write('K7:K7', '???')
    ws.write('L6:L6', 'Fev')

    ws.write('M6:M6', 'Mars')

    ws.write('N6:N6', str(dateFin)+' T2')

    ws.write('P6:P6', 'Avril')

    ws.write('Q6:Q6', 'Mai')

    ws.write('R6:R6', 'Juin')

    ws.merge_range('S6:S7', 'FACTURATION\nT3', wrap)
    ws.write('T6:T6', 'TOTAL H')

    ws.merge_range('U6:U7', 'TOTAL €')

    

    #affichage n°, nom, prenom
    row = 6
    i = 1
    for element in rows:
        #affichage n°, nom, prenom
        ws.write(row+i, 0, i, formatBasic)
        ws.write(row+i, 1, element[1]+" "+element[2], formatBasic)

        #affichage CP / CA
        if element[4]=='contrat pro':
            ws.write(row+i, 2, 'CP', formatCp)
        elif element[4] == 'contrat alt':
            ws.write(row+i, 2, 'CA', formatCp)
        else:
            ws.write(row+i, 2, '???', formatBasic)

        #affichage Tarif conv
        ws.write(row+i, 3, tarifConv)


        i = i+1


    wb.close()
    return 0