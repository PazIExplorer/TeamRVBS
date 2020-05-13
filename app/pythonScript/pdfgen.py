import sys
import os
from datetime import datetime
import shutil

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

from reportlab.pdfgen import canvas, textobject
from reportlab.lib.pagesizes import letter, A4

from reportlab.platypus import Paragraph



alternant = "test2"

def pdf(etu,master,presence,administration):
    
    from reportlab.lib.units import cm,inch
    usmb=os.path.join("./app/static/img",'logoUSMB2.png')
    fc=os.path.join("./app/static/img","logoFC.jpg")
    signaturePNG=os.path.join("./app/static/img","signature.png")
    
    president=administration[0][4] 
    SFC=administration[0][5] 
   
    master= master
    alternant=etu
    periodeDebut=administration[0][2]
    periodeFin=administration[0][3]

    pathPDF = "./app/static/pdf"
    pathArchive = "./app/static/archive"
    filename = alternant+" Attestation.pdf"
    currDate = datetime.now()
    c = canvas.Canvas(os.path.join(pathPDF,filename))
    #obtention de l'année scolaire
    debutScol=datetime.strptime(administration[0][0], '%d/%m/%Y').date()
    finScol=datetime.strptime(administration[0][1], '%d/%m/%Y').date()
    anneeScolaire=str(debutScol.year)+"/"+str(finScol.year)
    #calcul de la présence
    dateDebut=datetime.strptime(periodeDebut, '%d/%m/%Y').date()
    dateFin=datetime.strptime(periodeFin, '%d/%m/%Y').date()
    for i in range(0,len(presence)):
        presence[i] = list(presence[i])
        
        presence[i][3]=datetime.strptime(presence[i][3], '%d/%m/%Y').date()   
    presence = sorted(presence, key=lambda presence: presence[3])
    
    i=0
    while (i!=len(presence)):
        print(presence[i][3])
        if(presence[i][3] < dateDebut):
            presence.remove(presence[i])
        elif(presence[i][3]>dateFin): 
            presence.remove(presence[i])
        else:
            i+=1
    
    presenceVirtuel = len(presence)*7
    
    presenceEffective = 0
    for i in range(0,len(presence)):
        if(presence[i][0]!=3):
            presenceEffective+=4
        if(presence[i][1]!=3):
            presenceEffective+=3
    
    # origin x y en haut à gauche 
    c.translate(inch,inch)

    c.line(0,600,440,600)
    c.line(0,560,440,560)
    c.line(0,600,0,560)
    c.line(440,600,440,560)
    # Police basique
    c.setFont("Helvetica", 14)
    

    #Service formation continue
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0,660,"Service Formation Continue")
    c.setFont("Helvetica",12)
    c.drawString(0,643,"N° déclaration d'activité : 8273 P 000273")
    c.drawString(0,626,"SIRET : 197 308 588 000 15")
    #attestation de presence
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(230, 575, "ATTESTATION DE PRÉSENCE")
    #Je soussigné
    c.setFont("Helvetica",12)
    textobject=c.beginText(0,540)
    soussigne="Je soussigné "+ president +", Président de l'université Savoie Mont Blanc \natteste que le stagiaire: "
    for line in soussigne.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject) 
    c.setFont("Helvetica-Bold",12)
    c.drawCentredString(200,500,alternant)
    #inscription
    c.setFont("Helvetica",12)
    textobject=c.beginText(0,450)
    inscription="est inscrit en " + master + " \npour l'année " + anneeScolaire + " et a suivi les cours pour la période du " + periodeDebut + "\nau " + periodeFin + " selon détail ci-dessous :"
    for line in inscription.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)

    print(presenceVirtuel)
    print(presenceEffective)

    # TODO: VALEUR DES MOIS CONCERNÉS
    c.drawString(0,350, "TODO : Ajouter les valeurs des mois concernés sur l'attestation")
    
    c.setFont("Helvetica-Bold",12)
    c.drawString(0,325,"Soit un total de " + str(presenceEffective) + " heures de présence.")
    
    c.setFont("Helvetica",12)
    c.drawString(0,300,"Heures de cours prévues : "+ str(presenceVirtuel) + " heures.")

    c.drawString(200,150,"Le Bourget du Lac,le "+str(currDate.day) + "/" + str(currDate.month)+ "/" + str(currDate.year))
    # #ajoute la date
    c.drawString(0,120,"Signature du stagiaire")
    c.setFont("Helvetica-Bold",12)
    c.drawString(200,120,"Pour l'organisme de formation")
    c.setFont("Helvetica",12)
    c.drawString(200,105,"Pour le Président de l'Université Savoie Mont Blanc")
    c.drawString(200,75, "Le directeur du S.F.C")
    c.drawString(200,50,SFC)
    # change color
    c.setFillColorRGB(0,0,0)
    #ajout d'image
    c.drawImage(usmb,0,690,150,60)
    c.drawImage(fc,420,-30,250,50)
    c.drawImage(signaturePNG,280,-20,130,80)
    c.showPage()
    c.save()

    # ARCHIVAGE
    fichierAnneeScolaire = str(debutScol.year)+"-"+str(finScol.year)
    fichierDateDebut     = ("0"+str(dateDebut.day) if dateDebut.day<10 else str(dateDebut.day)) + "-" + ("0"+str(dateDebut.month) if dateDebut.month<10 else str(dateDebut.month)) + "-" + str(dateDebut.year)
    fichierDateFin       = ("0"+str(dateFin.day) if dateFin.day<10 else str(dateFin.day)) + "-" + ("0"+str(dateFin.month) if dateFin.month<10 else str(dateFin.month)) + "-" + str(dateFin.year)

    nomArchive = fichierAnneeScolaire + " " + master + " " + alternant + " du " + fichierDateDebut + " au " + fichierDateFin + " Attestation Présence"

    # Gestion des duplicatas
    if os.path.isfile(os.path.join(pathArchive,nomArchive) + ".pdf"):
        numDuplicata = 1
        while os.path.isfile(os.path.join(pathArchive,nomArchive) + " (" + str(numDuplicata) +").pdf"):
            numDuplicata+=1
        
        nomArchive += " (" + str(numDuplicata)+")"

    
    nomArchive += ".pdf" # Ajout de l'extension
    shutil.copy2(os.path.join(pathPDF,filename), os.path.join(pathArchive,nomArchive))
    return c



def presence(etu,master,presenceJour,administration):
    
    from reportlab.lib.units import cm,inch

    usmb=os.path.join("./app/static/img",'logoUSMB2.png')

    #obtention de l'année scolaire
    debutScol=datetime.strptime(administration[0][0], '%d/%m/%Y').date()
    finScol=datetime.strptime(administration[0][1], '%d/%m/%Y').date()
    anneeScolaire=str(debutScol.year)+"/"+str(finScol.year)

    master= master
    alternant=etu

    pathPDF = "./app/static/pdf"
    pathArchive = "./app/static/archive"
    filename = alternant+" Presence.pdf"

    periodeDebut=administration[0][2]
    periodeFin=administration[0][3]

    dateDebut=datetime.strptime(periodeDebut, '%d/%m/%Y').date()
    dateFin=datetime.strptime(periodeFin, '%d/%m/%Y').date()
   

    c = canvas.Canvas(os.path.join(pathPDF,filename))

    for i in range(0,len(presenceJour)):
        presenceJour[i] = list(presenceJour[i])
        
        presenceJour[i][3]=datetime.strptime(presenceJour[i][3], '%d/%m/%Y').date()
    presenceJour = sorted(presenceJour, key=lambda presence: presence[3])

    # origine x, y en haut à gauche
    c.translate(inch,inch)

    # Logo USMB
    c.drawImage(usmb,0,690,150,60)

    c.line(0,600,440,600)
    c.line(0,560,440,560)
    c.line(0,600,0,560)
    c.line(440,600,440,560)
    # Police basique
    c.setFont("Helvetica", 14)
    

    #Service formation continue
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0,660,"Service Formation Continue")
    c.setFont("Helvetica",12)
    c.drawString(0,643,"N° déclaration d'activité : 8273 P 000273")
    c.drawString(0,626,"SIRET : 197 308 588 000 15")
    #attestation de presence
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(230, 575, "FEUILLE DE PRÉSENCE")
    #Je soussigné
    c.setFont("Helvetica",12)
    textobject=c.beginText(0,540)
    soussigne="Le stagiaire: "
    for line in soussigne.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject) 
    c.setFont("Helvetica-Bold",12)
    c.drawCentredString(200,500,alternant)
    #inscription
    c.setFont("Helvetica",12)
    textobject=c.beginText(0,450)
    inscription="est inscrit en " + master + " \npour l'année " + anneeScolaire + " et a été présent sur les journées selon details ci dessous :"
    for line in inscription.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)

    #Affichage de l'ensemble des présences de l'étudiant traité 
    
    i=20
    for element in presenceJour:
        if(element[0]==2):
            if(element[1]==2):
                textobject.textLine(datetime.strftime(element[3],'%d/%m/%Y') +" - Absent journée ")
            else:
                textobject.textLine(datetime.strftime(element[3],'%d/%m/%Y')+" - Absent matin") 
        elif(element[1]==2):
            textobject.textLine(datetime.strftime(element[3],'%d/%m/%Y')+" - Absent après-midi")
        else:
            textobject.textLine(datetime.strftime(element[3],'%d/%m/%Y')+" - Présent")
        
        if(i%50==0):
            if (i-19 == len(presenceJour)):
                continue
            c.drawText(textobject)
            c.showPage()
            textobject=c.beginText(70,800)
            
        i+=1
    c.drawText(textobject)

    c.showPage()
    c.save()

    # ARCHIVAGE
    fichierAnneeScolaire = str(debutScol.year)+"-"+str(finScol.year)
    fichierDateDebut     = ("0"+str(dateDebut.day) if dateDebut.day<10 else str(dateDebut.day)) + "-" + ("0"+str(dateDebut.month) if dateDebut.month<10 else str(dateDebut.month)) + "-" + str(dateDebut.year)
    fichierDateFin       = ("0"+str(dateFin.day) if dateFin.day<10 else str(dateFin.day)) + "-" + ("0"+str(dateFin.month) if dateFin.month<10 else str(dateFin.month)) + "-" + str(dateFin.year)

    nomArchive = fichierAnneeScolaire + " " + master + " " + alternant + " du " + fichierDateDebut + " au " + fichierDateFin + " Feuille Présence"

    # Gestion des duplicatas
    if os.path.isfile(os.path.join(pathArchive,nomArchive) + ".pdf"):
        numDuplicata = 1
        while os.path.isfile(os.path.join(pathArchive,nomArchive) + " (" + str(numDuplicata) +").pdf"):
            numDuplicata+=1
        
        nomArchive += " (" + str(numDuplicata)+")"

    
    nomArchive += ".pdf" # Ajout de l'extension
    shutil.copy2(os.path.join(pathPDF,filename), os.path.join(pathArchive,nomArchive))
    return c
    return c
