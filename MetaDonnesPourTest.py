import pandas as pd
from statistics import stdev



file = "testExtrait.xml"
file2 = open('sortieUserMoyEcart.txt', "r")
fichierFinal = open('sortieFinal.txt', "w")  # contient la liste des moyennes et ecart type des users présent dans train et test
data = pd.read_xml(file)
commentaires = data['commentaire']   # commentaires
name = data['user_id'] # nom utilisateur
note = data['note'] # note

lines = file2.readlines()


for user in data['user_id']:
    for line in lines:
        if user in line:
            x=line.split()
            print(x)
            y=x[-2:]
            z = ' '.join(y)
            print(z)

            fichierFinal.write(str(user)+" "+str(z)+ " " + '\n')

        
fichierFinal.close()
file2.close()
