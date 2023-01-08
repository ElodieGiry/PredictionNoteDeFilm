import pandas as pd
import re

sortie = open("sortieSentimentPolarite.txt", "w")
file = "train.xml"
polariteFile="polariteSentiment.txt"
polarite = open(polariteFile, "r")
lines = polarite.readlines()
polarite_dict = {line.rsplit('"',maxsplit=4)[1].strip('"'): (line.rsplit(';',maxsplit=4)[2], line.rsplit(';',maxsplit=4)[3], line.rsplit(';',maxsplit=4)[4].strip()) for line in lines}
data = pd.read_xml(file)
commentaires = data['commentaire']   # commentaires

    
for i, commentaire in enumerate(commentaires):  # on parcours chaque commentaire
    print("coms",i)
    if commentaire is None:  # si le commentaire est vide
        sortie.write("\n")  # alors on écrit rien dans le fichier de sortie
    elif commentaire is not None:  # si le commentaire n'est pas vide
        commentaire_mots = commentaire.split()
        cpt = 0
        moy_positif = 0
        moy_negatif = 0
        moy_neutre = 0
        for mot in commentaire_mots:    # on parcours chaque mot du commentaire
            if mot in polarite_dict:
                cpt += 1
              #  print("test",polarite_dict[mot])
                p = int(polarite_dict[mot][0]) 
                ne = int(polarite_dict[mot][1]) 
                n = int(polarite_dict[mot][2]) 
                S = sum((p, ne, n))
                p = p / S 
                ne = ne / S
                n = n / S
                moy_positif += p
                moy_negatif += n
                moy_neutre += ne
        if cpt == 0: # si on ne trouve aucun mot du commentaire dans les mots polarité
            sortie.write("\n")
        else:   # sinon on ajoute la moyenne postif negatif et neutre de chaque mot
            moy_positif_final = moy_positif / cpt
            moy_neutre_final = moy_neutre / cpt
            moy_negative_final = moy_negatif / cpt
            sortie.write("2000001:{:.2f} 2000002:{:.2f} 2000003:{:.2f}\n".format(moy_positif_final, moy_neutre_final, moy_negative_final))

sortie.close()
