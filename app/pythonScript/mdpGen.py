#!/usr/bin/python
# -*-coding:utf-8 -*


from random import randint
import smtplib

def generateurMDP():
    caracteres="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    longueur=8
    mdp = ""
    i = 0
    while (i != longueur):
        i=i+1
        x=randint(0,62)
        mdp=mdp + caracteres[x]
    return mdp

def envoiMail(dest,mdp):
    serveur = smtplib.SMTP('smtp.gmail.com', 587)    ## Connexion au serveur sortant (en précisant son nom et son port)
    serveur.starttls()    ## Spécification de la sécurisation
    serveur.login("badgeuseusmb@gmail.com", "teamRVBS")    ## Authentification
    #message = ("Votre compte pour avoir accès au site de la badgeuse - User : " + dest + " --- Mot de passe : " + mdp).encode("utf-8")    ## Message à envoyer
    sujet = "Compte pour la badgeuse"
    message = u"""\
Bonjour,
Voici votre compte pour acceder au site de la badgeuse.
User : %s
Mot de passe : %s
""" % (dest,mdp)
    
    
    msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
""" % ("badgeuseUSMB <badgeuseusmb@gmail.com>",dest, sujet, message)
    serveur.sendmail("badgeuseusmb@gmail.com",str(dest),msg)    ## Envoie du message
    serveur.quit()    ## Déconnexion du serveur