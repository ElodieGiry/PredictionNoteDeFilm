from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import pandas as pd

sortie = open("polarite.txt", "w")
file = "train.xml"
data = pd.read_xml(file)
commentaires = data['commentaire']   # commentaires

# Créer un objet TextBlob à partir du commentaire
#commentaires="ce film est trop nul"
for coms in commentaires:
    if coms is not None:
        blob = TextBlob(coms)


# Obtenir la polarité et la subjectivité du commentaire
        polarity, subjectivity = blob.sentiment

# Déterminer si le commentaire est positif ou négatif
        
        if polarity > 0.1:
            print("Le commentaire est positif.")
            newPolarity=1
            sortie.write(str(newPolarity)+ "" + "\n")
        else:
            print("Le commentaire est négatif.")
            newPolarity=0
            sortie.write(str(newPolarity)+ "" + "\n")
    else:
        newPolarity=0
        sortie.write(str(newPolarity)+ "" + "\n")

