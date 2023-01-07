import pandas as pd


sortie = open("sortieSentimentPolarite.txt", "w")
file = "train.xml"
polariteFile="polariteSentiment.txt"
polarite = open(polariteFile, "r")
data = pd.read_xml(file)
commentaires = data['commentaire']   # commentaires
lines = polarite.readlines()
p=0
moyNegativeFinal=0
moyNeutreFinal=0
moyPositifFinal=0
motTrouve=0
cpt=0
nbCom=0
for commentaire in commentaires:  # on parcours chaque commentaire
     nbCom+=1
     moyPositif=0
     moyNegatif=0
     moyNeutre=0
    
     if commentaire is None:  # si le commentaire est vide
        sortie.write("\n")  # alors on écrit rien dans le fichier de sortie
     if commentaire is not None:  # si le commentaire n'est pas vide
        commentaireMot=commentaire.split()
        for mot in commentaireMot:    # on parcours chaque mot du commentaire
            for line in lines:  # on parcours chaque mot du fichier avec les polarité
                elements = line.split(';')
                if(len(elements)>2):
                    element_between_quotes = elements[1]
                    positif=elements[2]
                    neutre=elements[3]
                    negatif=elements[4]
                    clean_string = element_between_quotes.strip('"')   #enelever les guillemets du debut et de fin de chaque mot
                    if(clean_string==mot):  # si un mot du commentaire = à un mot de polarité
                        cpt+=1
                        S=int(positif)+int(neutre)+int(negatif)
                        p=int(positif)/S
                        ne=int(neutre)/S
                        n=int(negatif)/S
                        total=p+ne+n
                        moyPositif=(moyPositif+p)
                        moyNegatif=(moyNegatif+n)
                        moyNeutre=(moyNeutre+ne)
                        moyPositifFinal=moyPositif/cpt
                        moyNegativeFinal=moyNegatif/cpt
                        moyNeutreFinal=moyNeutre/cpt
                        moyPositifFinal=round(moyPositifFinal,2)
                        moyNeutreFinal=round(moyNeutreFinal,2)
                        moyNegativeFinal=round(moyNegativeFinal,2)

        if cpt == 0 : # si on ne trouve aucun mot du commentaire dans les mots polarité
            sortie.write("\n")
    
     
        else:   # sinon on ajoute la moyenne postif negatif et neutre de chaque mot 
            sortie.write("2000001:"+str(moyPositifFinal)+ " "+"2000002:"+str(moyNeutreFinal)+ " "+"2000003:"+ str(moyNegativeFinal) + str('\n'))
                     
           
        
sortie.close()
   

  
    



