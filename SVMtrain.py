# -*- coding: utf-8 -*-
import unidecode #supprime accents

#dicoTrain="dicoTrain.svm"
dicoTrain="dicoTrainMovie.txt"
fileTest="train.xml"
fileSVMNonTrouve="trainMovie.txt"

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

svmNonTrouve = open(fileSVMNonTrouve, "w", encoding="utf8")
fileSVM='trainDicoMovie.svm'
svm = open(fileSVM, "w", encoding="utf8")

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
        if nbCom % 10000 == 0:
            print("train.svm, commentaire :",nbCom)
        movie = fichier.readline() 
        review_id = fichier.readline()
        name = fichier.readline()
        user_id = fichier.readline()
        note = fichier.readline()[7:-8]
        note=note.replace(',','.')
        note=float(note)*2
        
        commentaire = fichier.readline()
        while commentaire[-15:]!="</commentaire>\n":
            commentaire = commentaire+fichier.readline()
        commentaire = commentaire[14:-15]
        
        if nbCom == 106077: 
            print("------------------------------------------------")
            print("commentaire avant transformation =",commentaire)
        
        #print("commentaire  de base = ",commentaire)
        finBloc = fichier.readline()
        bloc = fichier.readline()
        
        listeMot=commentaire.split()
        
        nouvelleListeMot=[]
        for mot in listeMot : 
           nouvelleListeMot.append(mot)
                
        listeMotsCommentaireSansDoublon = list(set(nouvelleListeMot))
        
        ligneSVMListe=[]
        
        for mot in listeMotsCommentaireSansDoublon:           
            occurence=nouvelleListeMot.count(mot)    
           
            
            #mettre mot sans MAJ , accents
            #print("---------------------------------------------------")
            #print("mot cherché : ",mot)
            
            indice=dictionnaireUnique.get(mot,0)
            if nbCom == 106077:
                print("mot  =",mot,"indice = ",indice,"occurence = ",occurence)
            
            #print("mot cherché",mot,"indice",indice)
            if(indice!=0):
                indexOccurence=[]
                indexOccurence.append(indice)
                indexOccurence.append(occurence)
                if nbCom == 106077:
                    print("indexOccurence = ",indexOccurence)
                ligneSVMListe.append(indexOccurence)
                
                nbMotTrouve=nbMotTrouve+1
                #print("trouvé")
            else:
                nbMotPasTrouve=nbMotPasTrouve+1
                svmNonTrouve.write(mot+"\n")
                #print("pas trouvé")
        #print("----------------------------------------------------")

        ligneSVMListe.sort()
        
        ligneSVMtmp=str(int(note))
        for ligne in ligneSVMListe:
            ligneSVMtmp=ligneSVMtmp+" "+str(ligne[0])+":"+str(ligne[1])
            if nbCom == 106077:
                print("ligneSVMtmp = ",ligneSVMtmp)
        ligneSVMtmp=ligneSVMtmp+"\n"
        svm.write(ligneSVMtmp)
   
print("Fichier lu : ",fileTest)       
print("Nb commentaires =",nbCom)
print ("Nb mots dictionnaire=",len(dictionnaireUnique))  

print("Nb Mot Trouve = ",nbMotTrouve)
print("Nb Mot Pas Trouve = ",nbMotPasTrouve)

print()
fichier.close()       
svm.close()
svmNonTrouve.close()
