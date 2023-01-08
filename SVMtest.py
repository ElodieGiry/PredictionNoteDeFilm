# -*- coding: utf-8 -*-
import unidecode #supprime accents
dicoTrain="dicoTrainMovie.txt"
fileTest="test.xml"
fileSVMNonTrouve="testMotNonTrouve.xml"
svmNonTrouve = open(fileSVMNonTrouve, "w", encoding="utf8")
fileSVM='testDicoMovie.svm'
svm = open(fileSVM, "w", encoding="utf8")

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

#Etape 1 lecture dictionnaire
dictionnaireUnique=dict()
nbCom=0
with open(dicoTrain, 'r', encoding='utf8') as fichier:
    mot = fichier.readline()
    while mot != "":
        mot=mot[:-1]
        nbCom+=1
        dictionnaireUnique[mot]=nbCom
        mot = fichier.readline()
fichier.close()
print("Fichier lu : ",dicoTrain) 
print("nombre de mots dans dictionnaire",nbCom) 

#Etape 2 constitution fichier svm
nbCom=0
nbMotPasTrouve=0
nbMotTrouve=0
with open(fileTest, 'r', encoding='utf8') as fichier:
    header = fichier.readline()
    bloc = fichier.readline()

    while (bloc=="<comment>\n"):
        nbCom=nbCom+1
        if nbCom % 1000 == 0:
            print("fabrique SVM commentaire numéro :",nbCom)
        movie = fichier.readline() 
        review_id = fichier.readline()
        name = fichier.readline()
        user_id = fichier.readline()
        commentaire = fichier.readline()
        while commentaire[-15:]!="</commentaire>\n":
            commentaire = commentaire+fichier.readline()
        commentaire = commentaire[14:-15]
        finBloc = fichier.readline()
        bloc = fichier.readline()   
        listeMotsCommentaire=commentaire.split()
        
        nouvelleListeMot=[]
        for mot in listeMotsCommentaire : 
           nouvelleListeMot.append(mot)
      
        listeMotsCommentaireSansDoublon = list(set(nouvelleListeMot))
        
        ligneSVMListe=[]
        
        for mot in listeMotsCommentaireSansDoublon:           
            occurence=nouvelleListeMot.count(mot)         
            
            indice=dictionnaireUnique.get(mot,0)
            if(indice!=0):
                indexOccurence=[]
                indexOccurence.append(indice)
                indexOccurence.append(occurence)   
                ligneSVMListe.append(indexOccurence)
                nbMotTrouve=nbMotTrouve+1
            else:
                nbMotPasTrouve=nbMotPasTrouve+1
                svmNonTrouve.write(mot+"\n")

        ligneSVMListe.sort()
        ligneSVMtmp="1"
        for ligne in ligneSVMListe:
            ligneSVMtmp=ligneSVMtmp+" "+str(ligne[0])+":"+str(ligne[1])
        ligneSVMtmp=ligneSVMtmp + " 1" +"\n"
        svm.write(ligneSVMtmp)
   
print("Fichier lu : ",fileTest)       
print("Nb commentaires =",nbCom)
print ("Nb mots dictionnaire trié=",len(dictionnaireUnique))  
print("Nb Mot Pas Trouvés = ",nbMotPasTrouve)
print("Nb Mot Trouvés = ",nbMotTrouve)

print()
fichier.close()       
svm.close()
svmNonTrouve.close()
