import sys
import os

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
    
    c = canvas.Canvas(os.path.join("./app/static/pdf",alternant+".pdf"))

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
    return c










