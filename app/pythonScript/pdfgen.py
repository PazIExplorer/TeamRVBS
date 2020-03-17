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

def pdf(etu,master):
    
    from reportlab.lib.units import cm,inch
    usmb=os.path.join("./app/static/img",'logoUSMB2.png')
    fc=os.path.join("./app/static/img","logoFC.jpg")
    signaturePNG=os.path.join("./app/static/img","signature.png")
    anneeScolaire="2019/2020"
    president="Denis VARASCHIN"
    SFC="ERIC WEISS"
   
    master= master
    alternant=etu
    periodeDebut="9 septembre 2019"
    periodeFin="13 décembre 2019"

    pathPDF = "./app/static/pdf"
    pathArchive = "./app/static/archive"
    filename = alternant+".pdf"
    
    c = canvas.Canvas(os.path.join(pathPDF,filename))

    # move the origin up and to the left
    c.translate(inch,inch)

    c.line(0,600,440,600)
    c.line(0,560,440,560)
    c.line(0,600,0,560)
    c.line(440,600,440,560)
    # define a large font
    c.setFont("Helvetica", 14)
    

    #Service formation continue
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0,660,"Service Formation Continue")
    c.setFont("Helvetica",12)
    c.drawString(0,643,"N° déclaration d'activité : 8273 P 000273")
    c.drawString(0,626,"SIRET : 197 308 588 000 15")
    #attestation de presence
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(230, 575, "ATTESTATION de PRÉSENCE")
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

    c.drawString(200,150,"Le Bourget du Lac,le ")
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
    currDate = datetime.now()
    dateStr = str(currDate.year) + "-" + str(currDate.month)+ "-" + str(currDate.day) + "-" + str(currDate.hour) + "-" + str(currDate.minute) + "-" + str(currDate.second) + "-" + filename
    shutil.copy2(os.path.join(pathPDF,filename), os.path.join(pathArchive,dateStr))
    return c



def presence(etu,master,presenceJour):
    
    from reportlab.lib.units import cm,inch
    anneeScolaire="2019/2020"
    master= master
    alternant=etu

    pathPDF = "./app/static/pdf"
    pathArchive = "./app/static/archive"
    filename = alternant+" Presence.pdf"
   

    c = canvas.Canvas(os.path.join(pathPDF,filename))

    for i in range(0,len(presenceJour)):
        presenceJour[i] = list(presenceJour[i])
        
        presenceJour[i][3]=datetime.strptime(presenceJour[i][3], '%d/%m/%Y').date()
    presenceJour = sorted(presenceJour, key=lambda presence: presence[3])
 
   


    
  
    
    

    # move the origin up and to the left
    c.translate(inch,inch)

    c.line(0,600,440,600)
    c.line(0,560,440,560)
    c.line(0,600,0,560)
    c.line(440,600,440,560)
    # define a large font
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
    currDate = datetime.now()
    dateStr = str(currDate.year) + "-" + str(currDate.month)+ "-" + str(currDate.day) + "-" + str(currDate.hour) + "-" + str(currDate.minute) + "-" + str(currDate.second) + "-" + filename
    shutil.copy2(os.path.join(pathPDF,filename), os.path.join(pathArchive,dateStr))
    return c
