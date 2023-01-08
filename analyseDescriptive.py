#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tqdm import tqdm
import pandas as pd
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import collections
import operator
try:
    stopwordsLibrairie = set(stopwords.words('french'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stopwordsLibrairie = set(stopwords.words('french'))
nltk.download('punkt')

###############################################################################
# Variable des mots à supprimer du dictionnaire
###############################################################################
stopword=["de","et","le","qui","à", "la", "un", "les", "pas", "que", "ce","en","des","au","une",
"alors", "au", "aucuns", "aussi", "autre", "avant", "avec", "avoir", "bon", "car", "ce", "cela", "ces", "ceux", "chaque", "ci",
"comme","comment","dans","des","du","dedans","dehors","depuis","devrait","doit","donc","dos","début","elle","elles","en",
"encore","essai","est","et","eu","fait","faites","fois","font","hors","ici","il","ils","je","juste","la","le","les","C'est",
"leur","là","ma","maintenant","mais","mes","mien","moins","mon","mot","même","ni","nommés","notre","nous","ou","où","On",
"par","parce","pas","peut","peu","plupart","pour","pourquoi","quand","que","quel","quelle","quelles","quels","qui","me",
"sa","sans","ses","seulement","si","sien","son","sont","sous","soyez","sujet","sur","ta","tandis","tellement","tels",
"tes","ton","tous","tout","trop","très","tu","voient","vont","votre","vous","vu","ça","étaient","état","étions","été","être",
"qu'", "d'être","vous","ce","En","se","c'est","n'est","en","n'ai","qu'on","Il","J'ai","Je","Une","Ce","aux","ont",
' ' , ',' , ':' , ';' , '.' , "'" , '-' , '!' , '?' ,"a", "ne","Le","on","cette","Un","j'ai","Et","d'un","d'une","La","qu'il","Les"]

###############################################################################
# Lecture du fichier et conversion des notes en float
###############################################################################
print("avant read_xml")
#Récupération des données train sur les commentaires de films

data = pd.read_xml("test.xml")
print("après read_xml")

#Transformation des virgules en points pour avoir les notes 
#en format float pour les statistiques
data['note'] = data['note'].str.replace(',','.').astype(float)

tabUserMeilleurNotation=dict()
tabUserNbNotes=dict()

tabContribution=[]
print("tab contribution et tab meilleure et pire notes")

userAndNote = data
userAndNote = userAndNote.drop(['movie', 'review_id','name','commentaire'], axis = 1)
compteNoteParUser = userAndNote.groupby('user_id')['note'].count()

contribUser=str(compteNoteParUser).split()

i=1
listeContrib=[]
while contribUser[i] != "Name:":
    if contribUser[i]=="...":
        i=i+1
    else:
        print("dans while",contribUser[i+1])
        i=i+2
   
print(listeContrib)

print(compteNoteParUser[:5])

cpt=0
for user in data["user_id"]: 
    cpt=cpt+1
    if cpt%1000==0:
        print("cpt",cpt)
    noteDuUser=data[data["user_id"]==user].note
    tabUserNbNotes[user]=len(noteDuUser)   
    tabContribution.append(len(noteDuUser))   
    
    tabNotes=str(noteDuUser).split()
    
    i=0
    tabNotesMoy=[]
    while tabNotes[i] != "Name:":
        if tabNotes[i]=="...":
            i=i+1
        else:
            tabNotesMoy.append(tabNotes[i+1])
            i=i+2
            
    somme=0
    for note in tabNotesMoy:
        note=float(note) 
        somme=somme+note
       
    moy=somme/len(tabNotesMoy)

    tabUserMeilleurNotation[user]=moy
    
    tabUserMeilleurNotationTrie= sorted(tabUserMeilleurNotation.items(), key=operator.itemgetter(1),reverse=True)
    #meilleurs note
    tabUserMeilleurNotation10 = list(tabUserMeilleurNotationTrie)[:10]
    #pires notes
    tabUserPireNotation10 = list(tabUserMeilleurNotationTrie)[10:]
 
print("tabContribution ", tabContribution)
print("avant boite moustache")
    
plt.boxplot(tabContribution)
plt.title("Distribution du nombre de contributions")
plt.savefig('analyse/boiteMoustacheContribution.png')
plt.show()   
 
print("10 utilisateurs ayant mis les meilleures notes :")
print(tabUserMeilleurNotation10)
print("10 utilisateurs ayant mis les pires notes :")
print(tabUserPireNotation10)

print("tabUserNbNotes[user]",tabUserNbNotes)
tabUserNbNotesTrie= sorted(tabUserNbNotes.items(), key=operator.itemgetter(1),reverse=True)

print("tabUserNbNotesTrie",tabUserNbNotesTrie)

meilleurContributeur = list(tabUserNbNotesTrie)[0]
print("meilleurContributeur = ",meilleurContributeur)

meilleurContributeur=str(meilleurContributeur).split('\'')

notemeilleurContributeur=data[data["user_id"]==meilleurContributeur[1]].note
print("key=",notemeilleurContributeur)

tabNotes=str(notemeilleurContributeur).split()
i=0
listeNoteMeilleurContributeur=[]
while tabNotes[i] != "Name:":
    if tabNotes[i]=="...":
        i=i+1
    else:
        listeNoteMeilleurContributeur.append(tabNotes[i+1])
        i=i+2
print("Liste note de meilleur contributeur",listeNoteMeilleurContributeur)

listeNoteMeilleurContributeurFloat=[]
for note in listeNoteMeilleurContributeur: 
    listeNoteMeilleurContributeurFloat.append(float(note))
plt.boxplot(listeNoteMeilleurContributeurFloat)

plt.ylim(0,5)
plt.title("Distribution des notes du meilleur contributeur")
plt.savefig('analyse/boiteMoustacheMeilleurContributeur.png')
plt.show()

##############################################################################
Lydia test stopwords
##############################################################################
try:
    french_stopwords = set(stopwords.words('french'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stopwords = set(stopwords.words('french'))
filtre_stopfr =  lambda text: [token for token in text if token.lower() not in french_stopwords]
data['commentaire'] = [' '.join(filtre_stopfr(word_tokenize(item))) for item in data['commentaire']]
print("filtrer")
print(data["commentaire"])

Statistique de base sur les notes
noteData = data['note']
print(data.dtypes)

#TF IDF dictionnaire
###############################################################################
# Variables
###############################################################################
#Initialise la liste de tous les commentaires du corpus
commentaires = data['commentaire']

###############################################################################
# Fonction qui retourne (dict)ionnaire pour commentaires pour 1 note donnée
###############################################################################
def sacDeMotParNote(note):
    print("debut sac de mot")
    dataUn = data[data["note"] == note]
    #dataUn = data[data["note"] == 0.5]
    commentaireDataUn = dataUn['commentaire']
    #print("commentaireDataUn",commentaireDataUn)
    dictionnaire =  []
    for commentaire  in commentaireDataUn:
        if commentaire is not None:
            dictionnaire.append(commentaire.split())
    print("fin sac de mot")
    return dictionnaire

def sacDeMot(commentaires):
    dictionnaire =  []
    for commentaire  in commentaires:
        if commentaire is not None:
            #print("*****")
            #print(commentaire)
            dictionnaire.append(commentaire.split())
    return dictionnaire

###############################################################################
# Fonction qui retourne paire mot / occurence mot de dictionnaire de mot
###############################################################################
#EG : TF IDF occurence mots
def repetitionMot(sacDeMot):
    wordsOccurences = dict()
    print("repetitionMot")
    #for mots in tqdm(sacDeMot,desc="la liste des mots"): 
    for mot in sacDeMot:
        
        if mot in wordsOccurences:
            wordsOccurences[mot] += 1
        else:
            wordsOccurences[mot] = 1
            
    return wordsOccurences

###############################################################################
# Fonction qui retourne les mots à plus de 3 caractères identiques succcessif
###############################################################################
listeRepet=[]   # liste pour stocké les mots avec caractères répétitifs
nbRepet=[]

def repet(dictionnaireParNote):
    i=0
    taille=0
    for mot in dictionnaireParNote:
        for mot1 in mot : 
            taille=len(mot1)-1
            if len(mot1)>=3: 
                        #print(mot1)
                if  mot1[i]==mot1[i+1] or mot1[taille]==mot1[taille-1]:
                    if mot1[i+1]==mot1[i+2] or mot1[taille-1]==mot1[taille-2]:
                            #print("mot = ",mot1)
                            listeRepet.append(mot1)
                            #print("repettttttttt",listeRepet)
    for element in listeRepet:
        x=listeRepet.count(element)
        nbRepet.append(x)
                     
#repet(sacDeMotParNote(5))

###############################################################################
# Fonction qui retourne la fréquence de : commentaire, movie, user_id (len(test)
###############################################################################
def frequenceData():
    cpt=0
    l=[]
    for user in data["user_id"]:
        l.append(user)
        cpt+=1
    
    print("Liste utilisateurs de base")
    print(l)
    print("Nombre utilisateurs de base")
    print(cpt)
    print("Nouvelle liste sans doublons et nombre")
    test=Counter(l).keys()
    print(test)
    print("nb comemntaire",cpt)
    print("nb de user " ,len(l))
    print(Counter(l).values())
    
###############################################################################
# Statistiques de base 
###############################################################################
def statistiqueBase():
    #Note minimale
    noteMin = noteData.min()
    print("Note minimale : ",noteMin)
    
    #Note maximale
    noteMax = noteData.max()
    print("Note maximale : ",noteMax)
    
    #Note médiane
    noteMedians = noteData.median()
    print("Note médiane : ",noteMedians)
    
    #Note moyenne
    noteMoyenne= noteData.mean()
    print("Note moyenne : ",noteMoyenne)
    
    #Note moyenne
    noteLaPlusFrequente = noteData.mode()
    print("Note la plus fréquente : ")
    print(noteLaPlusFrequente)
    
###############################################################################
# Graphique nuage de mots les plus fréquents
###############################################################################
def nuageDeMot():
    #Crée dictionnaire pour 1 note donnée
    #Parcourt toutes les valeurs des notes avec pas de 0.5
    for i in range (1,11,1):
        print("traitement note",i/2)
        motDico=[]
        dictionnaireParNote= sacDeMotParNote(i/2)
        #dictionnaireParNote= sacDeMotParNote(0.5)
        
        #Découpage des commentaires en mots et ajout dans le dictionnaire
        for mot in dictionnaireParNote:
            for mot1 in mot :
                if mot1 not in stopword and mot1 not in stopwordsLibrairie and len(mot1)>1:
                    motDico.append(mot1)
        print("apres creation motDico")     
        
        wordsOccurences = repetitionMot(motDico)   
        
        ##### Trie des mots pour avoir les mots les plus 25 frequents du corpus #####
        orderedWordsOccurencesurences= sorted(wordsOccurences.items(), key=operator.itemgetter(1),reverse=True)
        #print("orderedWordsOccurencesurences=")
        #print(orderedWordsOccurencesurences)
        mostUsedWord = list(orderedWordsOccurencesurences)[:25]
        print("mostUsedWord")
        print(mostUsedWord) 
        
        if len(mostUsedWord)>0:
            #Nuage de mots avec mots les plus fréquents
            #wordcloud fait des filtres (si plusieurs mots de la même racine, il en prends 1)
            keys = [k for k, v in mostUsedWord]
            
            all_text = ' '.join([text for text in keys])
            wordcloud = WordCloud(width=800, height=500,
                                  random_state=21, max_font_size=110).generate(all_text)
            plt.figure(figsize=(15, 12))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off');
            plt.title("Nuage de mots pour note "+str(i/2))
            plt.savefig('analyse/nuageMotsNote'+str(i))
            plt.show()
            plt.close()   
        else:
            print("Pas de note",i/2)

###############################################################################
# Histogramme taille commentaire moyen par notes
###############################################################################
def histogrammeTailleCommentaireMoyenParNote():
    tailleCommentaire=[]
    #Parcourt toutes les valeurs des notes avec pas de 0.5
    for i in range (0,11,1):
        note = data[data["note"] == i/2]
        #Récupère le commentaire associé à la note
        
        commentaire =note['commentaire']
        commentaireNote = note['commentaire'].astype(str).map(len)
        commentaireNote = commentaireNote.mean()
        tailleCommentaire.append(commentaireNote)
    
    notes = ('0','0.5','1','1.5','2','2.5','3','3.5','4','4.5','5')
    y_pos = np.arange(len(notes))
    
    #Create bars
    plt.bar(y_pos, tailleCommentaire)
    #Create names on the x-axis
    plt.xticks(y_pos, notes)
    plt.ylabel('nb caractères moyen')
    plt.xlabel('notes')
    plt.title('Taille moyenne des commentaires par notes')
    plt.savefig('analyse/histogramme')
    plt.show()
    plt.close()    

###############################################################################
# Histogramme mots répétitifs  

def test():
    print("dans construction histogramme")
    #Parcourt toutes les valeurs des notes avec pas de 0.5
    #for i in range (len(listeRepet)):
        
    caracRep = listeRepet
   
    y_pos = np.arange(len(caracRep))
    
    #Create bars
    plt.bar(y_pos, nbRepet)
    #Create names on the x-axis
    plt.xticks(y_pos, caracRep)
    plt.ylabel('Occurences')
    plt.xlabel('Mots')
    plt.title('Mots à caractères répétitifs')
    plt.savefig('analyse/histogrammeMotCaractereRepetitif')
    plt.show()
    plt.close() 
#test()

def boiteMoustacheNotes():
    
    note = data[data["note"] == i/2]
    #Récupère le commentaire associé à la note
    commentaireNote = note['commentaire'].astype(str).map(len)
    commentaireNote = commentaireNote.mean()
    
    #notes d'un user
    print("dans boite moustache")
    data = [1,2,3,4,5,6,7,8,9]
    
    plt.boxplot(data)
    
    plt.ylim(0,10)
    
    plt.savefig('analyse/boiteMoustacheNotes.png')
    plt.show()
boiteMoustacheNotes()
###############################################################################
# Fonction qui affiche l'histogramme de la fréquence user, loi Normale
###############################################################################
import scipy
import scipy.stats
bins=500
frequenceUtilisateur = data['user_id'].value_counts()
y, x = np.histogram(frequenceUtilisateur, bins=bins, density=True)
# Milieu de chaque classe
x = (x + np.roll(x, -1))[:-1] / 2.0

dist_name = "gamma"

# Paramètres de la loi
dist = getattr(scipy.stats, dist_name)

# Modéliser la loi
param = dist.fit(frequenceUtilisateur)

loc = param[-2]
scale = param[-1]
arg = param[:-2]

pdf = dist.pdf(x, loc=loc, scale=scale, *arg)

plt.figure(figsize=(12,8))
plt.plot(x, pdf, label=dist_name, linewidth=3) 

plt.legend()
plt.show()
plt.savefig('fig/frequenceUtilisateur')
plt.close()   

print("---------------------------------------------------------------------")
print("Main : Statistiques sur les commentaires des films Allo Ciné")
print("---------------------------------------------------------------------")
#repet(sacDeMotParNote(0.5))
frequenceData()
#histogrammeTailleCommentaireMoyenParNote()
#nuageDeMot()

#Histogramme profil user selon notes
#def histogrammeProfil():
