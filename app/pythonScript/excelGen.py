import xlsxwriter
import mysql.connector
from app.pythonScript import fonctionPy

from app.pythonScript import config

def creation(idFiliere):
    #connection bdd
    cnx = mysql.connector.connect(host=config.BDD_host, database=config.BDD_database, user=config.BDD_user, password=config.BDD_password)
    cursor = cnx.cursor()

    query = ("SELECT * FROM administration")
    cursor.execute(query)
    recup = cursor.fetchall()

    #normalement ici il n'a récup qu'une ligne
    for element in recup:
        du = element[0]
        au = element[1]
        tarif = element[6]

    dateDebut = du[6]+du[7]+du[8]+du[9]
    dateFin = au[6]+au[7]+au[8]+au[9]
    tarifConv = str(tarif)+"€"   

    #Création du fichier et de la feuille
    wb = xlsxwriter.Workbook('app/static/excel/forfaitHorraire.xlsx') #création d'un classeur
    ws = wb.add_worksheet()

    #Déclaration des formats
    formatBasic = wb.add_format({'border':1})

    formatBold = wb.add_format()
    formatBold.set_bold()
    formatBold.set_border(1)
    
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
    formatT1Bold.set_align('center')

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
    formatT2Bold.set_align('center')

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
    formatT3Bold.set_align('center')

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
    ws.set_column('T:T', 14)
    ws.set_column('U:U', 10)
    ws.set_column('V:V', 11)

    #Créations de l'en-tête 
    ws.merge_range('B3:F3', 'RECAPITULATIF DES HEURES SUIVIES PAR STAGIARES EN M2 ISC _ 400 HEURES')
    ws.write('B1:B1', "SFC "+str(dateDebut)+"/"+str(dateFin))
    ws.merge_range('H3:J3', 'du '+du+' au '+ au)

    #Récupération des étudiants de la base
    #Récupérer les CP
    query = ("SELECT * FROM etudiant WHERE filiere = "+str(idFiliere)+" AND typeContratEtudiant = 'contrat pro' ORDER BY nom, prenom")
    cursor.execute(query)
    rowsCP = cursor.fetchall()

    #Récupérer les CA
    query = ("SELECT * FROM etudiant WHERE filiere = "+str(idFiliere)+" AND typeContratEtudiant = 'contrat appr' ORDER BY nom, prenom")
    cursor.execute(query)
    rowsCA = cursor.fetchall()


    #affichage des titres du tableau
    ws.merge_range('C6:C7', 'CP/CA', formatBasic)
    ws.merge_range('D6:D7', 'TARIF\nCONV.', formatT1BoldTitle)
    ws.write('E6:E6', 'Sept', formatT1BoldTitle)
    ws.write('F6:F6', 'Oct', formatT1BoldTitle)
    ws.write('G6:G6', 'Nov', formatT1BoldTitle)
    ws.write('H6:H6', 'Déc', formatT1BoldTitle)
    ws.write('I6:I6', str(dateDebut)+' T1', formatT1BoldTitle)
    ws.merge_range('J6:J7', 'FACTURATION\nT1', formatT1BoldTitle)
    ws.write('K6:K6', 'Janv', formatT2BoldTitle)
    ws.write('L6:L6', 'Fev', formatT2BoldTitle)
    ws.write('M6:M6', 'Mars', formatT2BoldTitle)
    ws.write('N6:N6', str(dateFin)+' T2', formatT2BoldTitle)
    ws.merge_range('O6:O7', 'FACTURATION\nT2', formatT2BoldTitle)
    ws.write('P6:P6', 'Avril', formatT3BoldTitle)
    ws.write('Q6:Q6', 'Mai', formatT3BoldTitle)
    ws.write('R6:R6', 'Juin', formatT3BoldTitle)
    ws.write('S6:S6', str(dateFin)+' T3', formatT3BoldTitle)
    ws.merge_range('T6:T7', 'FACTURATION\nT3', formatT3BoldTitle)
    ws.write('U6:U6', 'TOTAL H', formatTotalBoldTitle)
    ws.merge_range('V6:V7', 'TOTAL €', formatTotalBoldTitle)

    #afficher le nombre d'heures de cours par mois 
    tabHeure = fonctionPy.tabHeureCoursParMois(dateDebut, dateFin)
    #tableau de la forme {"Sept":0, "Oct":0, "Nov":0, "Déc":0, "Jan":0, "Fev":0, "Mars":0, "Avril":0, "Mai":0, "Juin":0} avec les 0 remplacés par le nb d'heures
    ws.write('E7:E7', str(tabHeure["Sept"]), formatT1Bold)
    ws.write('F7:F7', str(tabHeure["Oct"]), formatT1Bold)
    ws.write('G7:G7', str(tabHeure["Nov"]), formatT1Bold)
    ws.write('H7:H7', str(tabHeure["Déc"]), formatT1Bold)
    sommeT1 = "=E7+F7+G7+H7"
    ws.write_formula('I7:I7', sommeT1, formatT1Bold)

    ws.write('K7:K7', str(tabHeure["Jan"]), formatT2Bold)
    ws.write('L7:L7', str(tabHeure["Fev"]), formatT2Bold)
    ws.write('M7:M7', str(tabHeure["Mars"]), formatT2Bold)
    sommeT2 = "=K7+L7+M7"
    ws.write_formula('N7:N7', sommeT2, formatT2Bold)

    ws.write('P7:P7', str(tabHeure["Avril"]), formatT3Bold)
    ws.write('Q7:Q7', str(tabHeure["Mai"]), formatT3Bold)
    ws.write('R7:R7', str(tabHeure["Juin"]), formatT3Bold)
    sommeT3 = "=P7+Q7+R7"
    ws.write_formula('S7:S7', sommeT3, formatT3Bold)

    sommeTotal = "=I7+N7+S7"
    ws.write_formula('U7:U7', sommeTotal, formatTotalBold)
    
    #Affichage des CP :
    row = 6
    i = 1
    for element in rowsCP:
        #affichage n°, nom, prenom
        ws.write(row+i, 0, i, formatBasic)
        ws.write(row+i, 1, element[1]+" "+element[2], formatBasic)
        ws.write(row+i, 2, 'CP', formatCp)

        #affichage Tarif conv
        ws.write(row+i, 3, str(tarifConv), formatT1Base)

        #afficher la présence
        tab = fonctionPy.heurePresentParMois(element[3])
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
        ws.write_formula(row+i, 8, formule1, formatT1Bold)

        formule2 = "=K"+str(lc)+"+L"+str(lc)+"+M"+str(lc)
        ws.write_formula(row+i, 13,formule2, formatT2Bold)

        formule3 = "=P"+str(lc)+"+Q"+str(lc)+"+R"+str(lc)
        ws.write_formula(row+i, 18, formule3, formatT3Bold)

        #Formule pour le total
        formuleTotalHeure = "=I"+str(lc)+"+N"+str(lc)+"+S"+str(lc)
        ws.write_formula(row+i, 20, formuleTotalHeure, formatTotalBold)

        formuleTotalEuro = "=J"+str(lc)+"+O"+str(lc)+"+T"+str(lc)
        ws.write_formula(row+i, 21, formuleTotalEuro, formatTotalBold)



        #Pour la colonne facturation des CP pas de formule, complété a la main par la secrétaire
        ws.write("J"+str(row+i+1), "", formatT1Base)
        ws.write("O"+str(row+i+1), "", formatT2Base)
        ws.write("T"+str(row+i+1), "", formatT3Base)

        i = i+1


    #la ligne de séparation
    num = 1
    #Affichage des CA
    for element in rowsCA:
        #affichage n°, nom, prenom
        ws.write(row+i, 0, num, formatBasic)
        ws.write(row+i, 1, element[1]+" "+element[2], formatBasic)
    
        ws.write(row+i, 2, 'CA', formatCa)

        #affichage Tarif conv
        ws.write(row+i, 3, str(tarifConv), formatT1Base)

        #afficher la présence
        tab = fonctionPy.heurePresentParMois(element[3])
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
        ws.write_formula(row+i, 8, formule1, formatT1Bold)

        formule2 = "=K"+str(lc)+"+L"+str(lc)+"+M"+str(lc)
        ws.write_formula(row+i, 13,formule2, formatT2Bold)

        formule3 = "=P"+str(lc)+"+Q"+str(lc)+"+R"+str(lc)
        ws.write_formula(row+i, 18, formule3, formatT3Bold)

        #Formule pour le total
        formuleTotalHeure = "=I"+str(lc)+"+N"+str(lc)+"+S"+str(lc)
        ws.write_formula(row+i, 20, formuleTotalHeure, formatTotalBold)

        formuleTotalEuro = "=J"+str(lc)+"+O"+str(lc)+"+T"+str(lc)
        ws.write_formula(row+i, 21, formuleTotalEuro, formatTotalBold)

        formuleTotalTrimestre = "="+str(tarif)+"/3"

        #formule pour la facturation CA
        ws.write_formula("J"+str(row+i+1), formuleTotalTrimestre, formatT1Bold)
        ws.write_formula("O"+str(row+i+1), formuleTotalTrimestre, formatT2Bold)
        ws.write_formula("T"+str(row+i+1), formuleTotalTrimestre, formatT3Bold)

        #incrémentation des var
        num = num+1
        i = i+1







    #Formule pour le total
    ws.write("C"+str(row+i+1), "", formatBasic)
    ws.write("D"+str(row+i+1), "", formatT1Base)
    ws.write(row+i, 1, "Totaux présence :", formatBasic)
    ws.write_formula(row+i, 4, "=SUM(E8:E"+str(7+i-1)+")", formatT1Base)
    ws.write_formula(row+i, 5, "=SUM(F8:F"+str(7+i-1)+")", formatT1Base)
    ws.write_formula(row+i, 6, "=SUM(G8:G"+str(7+i-1)+")", formatT1Base)
    ws.write_formula(row+i, 7, "=SUM(H8:H"+str(7+i-1)+")", formatT1Base)
    ws.write_formula(row+i, 8, "=SUM(I8:I"+str(7+i-1)+")", formatT1Base)
    ws.write(row+i, 9, "", formatT1Bold)
    ws.write_formula(row+i, 10, "=SUM(K8:K"+str(7+i-1)+")", formatT2Base)
    ws.write_formula(row+i, 11, "=SUM(L8:L"+str(7+i-1)+")", formatT2Base)
    ws.write_formula(row+i, 12, "=SUM(M8:M"+str(7+i-1)+")", formatT2Base)
    ws.write_formula(row+i, 13, "=SUM(N8:N"+str(7+i-1)+")", formatT2Base)
    ws.write(row+i, 14, "", formatT2Bold)
    ws.write_formula(row+i, 15, "=SUM(P8:P"+str(7+i-1)+")", formatT3Base)
    ws.write_formula(row+i, 16, "=SUM(Q8:Q"+str(7+i-1)+")", formatT3Base)
    ws.write_formula(row+i, 17, "=SUM(R8:R"+str(7+i-1)+")", formatT3Base)
    ws.write_formula(row+i, 18, "=SUM(S8:S"+str(7+i-1)+")", formatT3Bold)
    ws.write(row+i, 19, "", formatT3Bold)
    ws.write(row+i, 20, "", formatTotalBase)
    ws.write(row+i, 21, "", formatTotalBase)
   
    ws.set_row(row+i, 24)


    ws.write(row+i+1, 9, "", formatT1Bold)
    ws.write(row+i+1, 14, "", formatT2Bold)
    ws.write(row+i+1, 19, "", formatT3Bold)
    ws.write(row+i+1, 20, "", formatTotalBold)
    ws.write(row+i+1, 21, "", formatTotalBold)
    ws.write(row+i+2, 1, "FACTURATION trimestrielle heures suivies", formatBold)

    ws.write(row+i+1, 1, "", formatBasic)
    for a in range(2, 9):
        ws.write(row+i+1, a, "", formatBasic)
        ws.write(row+i+2, a, "", formatBasic)

    for a in range(10, 14):
        ws.write(row+i+1, a, "", formatBasic)
        ws.write(row+i+2, a, "", formatBasic)

    for a in range(15, 19):
        ws.write(row+i+1, a, "", formatBasic)
        ws.write(row+i+2, a, "", formatBasic)


    ws.write_formula(row+i+2, 9, "=SUM(J8:J"+str(7+i-1)+")", formatT1Bold)
    ws.write_formula(row+i+2, 14, "=SUM(O8:O"+str(7+i-1)+")", formatT2Bold)
    ws.write_formula(row+i+2, 19, "=SUM(T8:T"+str(7+i-1)+")", formatT3Bold)
    ws.write_formula(row+i+2, 20, "=SUM(U8:U"+str(7+i-1)+")", formatTotalBold)
    ws.write_formula(row+i+2, 21, "=SUM(V8:V"+str(7+i-1)+")", formatTotalBold)
    ws.set_row(row+i+1, 24)
   
    
    wb.close()
    return 0