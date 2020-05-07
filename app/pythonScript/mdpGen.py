#!/usr/bin/python
# -*-coding:utf-8 -*

from random import randint
import smtplib

from app.pythonScript import config

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
    serveur = smtplib.SMTP(config.MAIL_host, config.MAIL_port) # Connexion au serveur (en précisant son nom et son port)
    serveur.starttls()
    serveur.login(config.MAIL_usermail, config.MAIL_password) # Authentification
    sujet = "Compte pour la badgeuse"
    message = u"""\
Bonjour,
Voici votre compte pour acceder au site de la badgeuse.

Adresse du site : http://mau-59-pointeuse.local.univ-savoie.fr/
Site accessible au travers du VPN universitaire : vpn.univ-savoie.fr

User : %s
Mot de passe : %s
""" % (dest,mdp)

    user =  config.MAIL_username + " <" + config.MAIL_usermail + ">"   # Ressemble à "NomCompte <adresse@mail.fr>"
    
    msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
""" % (user, dest, sujet, message)
    serveur.sendmail(config.MAIL_usermail,str(dest),msg) # Envoi du message
    serveur.quit() # Déconnexion du serveur



def envoiMailModif(dest,mdp):
    serveur = smtplib.SMTP(config.MAIL_host, config.MAIL_port) # Connexion au serveur (en précisant son nom et son port)
    serveur.starttls()
    serveur.login(config.MAIL_usermail, config.MAIL_password) # Authentification
    sujet = "Modification de votre mot de passe pour la badgeuse"
    message = u"""\
Bonjour,
Votre mot de passe pour acceder au site de la badgeuse est modifie.
Voici vos nouveaux identifiants.

Adresse du site : http://mau-59-pointeuse.local.univ-savoie.fr/
Site accessible au travers du VPN universitaire : vpn.univ-savoie.fr

User : %s
Mot de passe : %s
""" % (dest,mdp)
    

    user =  config.MAIL_username + " <" + config.MAIL_usermail + ">"   # Ressemble à "NomCompte <adresse@mail.fr>"

    msg = """\
From: %s\r\n\
To: %s\r\n\
Subject: %s\r\n\
\r\n\
%s
""" % (user, dest, sujet, message)
    serveur.sendmail(config.MAIL_usermail,str(dest),msg) # Envoi du message
    serveur.quit() # Déconnexion du serveur