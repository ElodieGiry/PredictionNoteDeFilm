# -*- coding: utf-8 -*-
#Lit fichier train et ecrit le dictionnaire correspondant
#TODO: dico à modifier (accent, maj, ", ', stopword, tokenisation)

import unidecode #supprime accents

fileIn="trainExtrait.xml"
fileOut='dicoTrainSansMajAccent.txt'
listeCaractere=["+", "[", "]", "$","%","#", "~", "{", "}", "|", "'","^","=",">","<",";","!","?","(",")",",","*","_","-",":","\\","/","."," ","&","\""]

stopwords = ['ai', 'alors', 'au', 'aucuns', 'aussi', 'autre', 'aux', 'avant', 'avec', 'avoir', 'bon', 'ca', 
             'car', 'ce', 'cela', 'ces', 'cette', 'ceux', 'chaque', 'ci', 'comme', 'comment', 'dans', 'de', 
             'debut', 'dedans', 'dehors', 'depuis', 'des', 'devrait', 'doit', 'donc', 'dos', 'du', 'elle', 
             'elles', 'en', 'encore', 'essai', 'est', 'et', 'etaient', 'etat', 'ete', 'etions', 'etre', 'eu', 
             'fait', 'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'je', 'juste', 'la', 'le', 'les', 
             'leur', 'ma', 'maintenant', 'mais', 'me', 'meme', 'mes', 'mien', 'moins', 'mon', 'mot', 'ne', 'ni', 
             'nommes', 'notre', 'nous', 'on', 'ont', 'ou', 'par', 'parce', 'pas', 'peu', 'peut', 'plupart', 'pour', 
             'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'se', 'ses', 
             'seulement', 'si', 'sien', 'son', 'sont', 'sous', 'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 
             'tels', 'tes', 'ton', 'tous', 'tout', 'tres', 'trop', 'tu', 'un', 'une', 'voient', 'vont', 'votre', 'vous', 'vu']

svm = open(fileOut, "w", encoding="utf8")
#dictionnaireUnique=[]
dictionnaireUnique=dict()
nbCom=0
indiceMot=0
with open(fileIn, 'r', encoding='utf8') as fichier:
    header = fichier.readline()
    bloc = fichier.readline()
    while (bloc=="<comment>\n"):
        nbCom=nbCom+1
        if nbCom % 1000 == 0:
            print("fabrique dictionnaire commentaire numéro :",nbCom)
        dictionnaireLigne =  []
        movie = fichier.readline() 
        review_id = fichier.readline()
        name = fichier.readline()
        user_id = fichier.readline()
        note = fichier.readline()[7:-8]
        commentaire = fichier.readline()
        #traitement des commentaires avec des \n
        while commentaire[-15:]!="</commentaire>\n":
            commentaire = commentaire+fichier.readline()
        commentaire = commentaire[14:-15]
        finBloc = fichier.readline()
        bloc = fichier.readline()
        listeMotsCommentaire=commentaire.split()
        for mot in listeMotsCommentaire:
    
            motSansAccent = unidecode.unidecode(mot.lower())
            #print("mot de base = ",motSansAccent)    
                    
            # nouveauMot=""
            # for caractere in motSansAccent :
            #     if caractere not in listeCaractere :
            #         nouveauMot = nouveauMot + caractere
            #     else : 
            #         nouveauMot = nouveauMot + " "
            
            # listeMot= nouveauMot.split()
            #print("split = ",listeMot)
            
            for mot in listeMotsCommentaire:
            #for mot in listeMot :
                if len(mot) >1 and mot not in stopwords:
                    indiceMot=indiceMot+1
                    dictionnaireUnique[mot]=len(dictionnaireUnique)
                
dictionnaireUnique=sorted(dictionnaireUnique)

for mot in dictionnaireUnique:
    svm.write(mot+"\n")
#print ("\Dictionnaire tri=\n",dictionnaireUnique)   
print ("\nNb mots dictionnaire trié=",len(dictionnaireUnique)) 
fichier.close()   
svm.close()