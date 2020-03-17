import xlsxwriter
import mysql.connector
from app.pythonScript import fonctionPy

def creation():
    #VALEUR A MODIFIER
    dateDebut = 2019
    dateFin = 2020
    du = '09/09/2019'
    au = '08/09/2020'
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

    formatCa = wb.add_format() #Format pour CA
    formatCa.set_border(1)
    formatCa.set_align('center')
    formatCa.set_font_color('red')

    formatT1Base = wb.add_format() #Format pour le t1
    formatT1Base.set_border(1)
    formatT1Base.set_bg_color('#D7EAFB')

    formatT1Bold = wb.add_format()
    formatT1Bold.set_border(1)
    formatT1Bold.set_bold()
    formatT1Bold.set_bg_color('#D7EAFB')

    formatT1BoldTitle = wb.add_format()
    formatT1BoldTitle.set_border(1)
    formatT1BoldTitle.set_bold()
    formatT1BoldTitle.set_bg_color('#D7EAFB')
    formatT1BoldTitle.set_align('center')
    formatT1BoldTitle.set_text_wrap(True)

    formatT2Base = wb.add_format() #Format pour le t2
    formatT2Base.set_border(1)
    formatT2Base.set_bg_color('#E2EFDA')

    formatT2Bold = wb.add_format()
    formatT2Bold.set_border(1)
    formatT2Bold.set_bold()
    formatT2Bold.set_bg_color('#E2EFDA')

    formatT2BoldTitle = wb.add_format()
    formatT2BoldTitle.set_border(1)
    formatT2BoldTitle.set_bold()
    formatT2BoldTitle.set_bg_color('#E2EFDA')
    formatT2BoldTitle.set_align('center')
    formatT2BoldTitle.set_text_wrap(True)

    formatT3Base = wb.add_format() #Format pour le t3
    formatT3Base.set_border(1)
    formatT3Base.set_bg_color('#D5D5FF')

    formatT3Bold = wb.add_format()
    formatT3Bold.set_border(1)
    formatT3Bold.set_bold()
    formatT3Bold.set_bg_color('#D5D5FF')

    formatT3BoldTitle = wb.add_format()
    formatT3BoldTitle.set_border(1)
    formatT3BoldTitle.set_bold()
    formatT3BoldTitle.set_bg_color('#D5D5FF')
    formatT3BoldTitle.set_align('center')
    formatT3BoldTitle.set_text_wrap(True)

    formatTotalBase = wb.add_format() #Format pour le Total
    formatTotalBase.set_border(1)
    formatTotalBase.set_bg_color('#FFDDFF')

    formatTotalBold = wb.add_format()
    formatTotalBold.set_border(1)
    formatTotalBold.set_bold()
    formatTotalBold.set_bg_color('#FFDDFF')

    formatTotalBoldTitle = wb.add_format()
    formatTotalBoldTitle.set_border(1)
    formatTotalBoldTitle.set_bold()
    formatTotalBoldTitle.set_bg_color('#FFDDFF')
    formatTotalBoldTitle.set_align('center')
    formatTotalBoldTitle.set_text_wrap(True)

    #Déclaration des dimensions des cellules
    ws.set_column('A:A', 2)
    ws.set_column('B:B', 37)
    ws.set_column('C:C', 7)
    ws.set_column('D:D', 9)
    ws.set_column('J:J', 14)
    ws.set_column('O:O', 14)
    ws.set_column('S:S', 14)
    ws.set_column('T:T', 10)
    ws.set_column('U:U', 11)

    #Créations de l'en-tête 
    ws.merge_range('B3:J3', 'RECAPITULATIF DES HEURES SUIVIES PAR STAGIARES EN M2 ISC _ 400 HEURES')
    ws.write('B1:B1', "SFC "+str(dateDebut)+"/"+str(dateFin))
    ws.merge_range('H3:J3', 'du '+du+' au '+ au)

    #Récupération des étudiants de la base
    #Récupérer les CP
    query = ("SELECT * FROM etudiant")
    cursor.execute(query)
    rows = cursor.fetchall()
    #Ré


    #affichage des titres du tableau
    ws.merge_range('C6:C7', 'CP/CA')
    ws.merge_range('D6:D7', 'TARIF\nCONV.', formatT1BoldTitle)
    ws.write('E6:E6', 'Sept', formatT1BoldTitle)
    ws.write('E7:E7', '???', formatT1Bold)
    ws.write('F6:F6', 'Oct', formatT1BoldTitle)
    ws.write('F7:F7', '???', formatT1Bold)
    ws.write('G6:G6', 'Nov', formatT1BoldTitle)
    ws.write('G7:G7', '???', formatT1Bold)
    ws.write('H6:H6', 'Déc', formatT1BoldTitle)
    ws.write('H7:H7', '???', formatT1Bold)
    ws.write('I6:I6', str(dateDebut)+' T1', formatT1BoldTitle)
    ws.write('I7:I7', '???', formatT1Bold)
    ws.merge_range('J6:J7', 'FACTURATION\nT1', formatT1BoldTitle)
    ws.write('K6:K6', 'Janv', formatT2BoldTitle)
    ws.write('K7:K7', '???', formatT2Bold)
    ws.write('L6:L6', 'Fev', formatT2BoldTitle)
    ws.write('L7:L7', '???', formatT2Bold)
    ws.write('M6:M6', 'Mars', formatT2BoldTitle)
    ws.write('M7:M7', '???', formatT2Bold)
    ws.write('N6:N6', str(dateFin)+' T2', formatT2BoldTitle)
    ws.write('N7:N7', '???', formatT2Bold)
    ws.merge_range('O6:O7', 'FACTURATION\nT2', formatT2BoldTitle)
    ws.write('P6:P6', 'Avril', formatT3BoldTitle)
    ws.write('P7:P7', '???', formatT3Bold)
    ws.write('Q6:Q6', 'Mai', formatT3BoldTitle)
    ws.write('Q7:Q7', '???', formatT3Bold)
    ws.write('R6:R6', 'Juin', formatT3BoldTitle)
    ws.write('R7:R7', '???', formatT3Bold)
    ws.merge_range('S6:S7', 'FACTURATION\nT3', formatT3BoldTitle)
    ws.write('T6:T6', 'TOTAL H', formatTotalBoldTitle)
    ws.write('T7:T7', '???', formatTotalBold)
    ws.merge_range('U6:U7', 'TOTAL €', formatTotalBoldTitle)

    

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
        ws.write(row+i, 3, str(tarifConv), formatT1Base)

        #afficher la présence
        tab = fonctionPy.heurePresentParMoi(element[0])
        ws.write(row+i, 4, tab["Sept"], formatT1Base)
        ws.write(row+i, 5, tab["Oct"], formatT1Base)
        ws.write(row+i, 6, tab["Nov"], formatT1Base)
        ws.write(row+i, 7, tab["Déc"], formatT1Base)
        ws.write(row+i, 10, tab["Jan"], formatT2Base)
        ws.write(row+i, 11, tab["Fev"], formatT2Base)
        ws.write(row+i, 12, tab["Mars"], formatT2Base)
        ws.write(row+i, 15, tab["Avril"], formatT3Base)
        ws.write(row+i, 16, tab["Mai"], formatT3Base)
        ws.write(row+i, 17, tab["Juin"], formatT3Base)
       

        #formule pour calculer la somme de chaque Trimestre
        lc = row+i+1
        formule1 = "=E"+str(lc)+"+F"+str(lc)+"+G"+str(lc)+"+H"+str(lc)
        ws.write_formula(row+i, 8, formule1, formatT1Base)

        formule2 = "=K"+str(lc)+"+L"+str(lc)+"+M"+str(lc)
        ws.write_formula(row+i, 13,formule2, formatT2Base)

        formule3 = "=P"+str(lc)+"+Q"+str(lc)+"+R"+str(lc)
        ws.write_formula(row+i, 18, formule3, formatT3Base)

        #TODO complete les cases vide que je ne comprend pas l'utilité avec le format
        ws.write("J"+str(row+i+1), "", formatT1Base)
        ws.write("O"+str(row+i+1), "", formatT2Base)

        i = i+1


    i = i+2
    ws.write(row+i, 1, "FACTURATION trimestrielle heures suivies")
    wb.close()
    return 0