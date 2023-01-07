import pandas as pd
from statistics import stdev

sortie2 = open("sortieUserMoyEcart.txt", "w")
file = "train_Extrait.xml"
data = pd.read_xml(file)
commentaires = data['commentaire']   # commentaires
name = data['user_id'] # nom utilisateur
note = data['note'] # note

listeNomNote=[]
listeNom=[]
listeNote=[]
listeFinal=[]

for user in data["user_id"]:  # recupere chaque users
    listeNom.append(user)


for note in data["note"]:  # recupere chaque note
    listeNote.append(note)
    

for x, y in zip(listeNom, listeNote):  # stocke users,note
    listeNomNote.append([x, y])  


result = {}

for lst in listeNomNote:
    key = lst[0]
    value = lst[1]
    if key in result:
        result[key].append(value)
    else:
        result[key] = [value]

L4 = [[key] + result[key] for key in result]


for l in L4:
    somme=0
    moyenne=0
    nouvelleListe=[]
    nom=l[0:1]
    nom=str(nom)
    liste=[] # pour stocké les notes pour l'ecart type

  # S'il y a au moins deux éléments dans la sous-liste (le premier étant la chaîne de caractères )
    if len(l) >= 3:
        cpt=0
        for note in l[1:]:
            nouvelleListe.append(l[0:1])
            liste.append(note)
            cpt=cpt+1
            note=note.replace(',','.')
            note=float(note)
            somme=somme+note
        numbers = []
        for note in liste:
            note=note.replace(',','.')
            note=float(note)
            numbers.append(int(note))

     
        ecartTyp=stdev(numbers)
        ecartTyp=round(ecartTyp,2)
        moyenne=somme/cpt
        moyenne=round(moyenne,2)
  
        nouvelleListe.append(moyenne)
        sortie2.write(nom[2:-2]+" "+str(moyenne)+" "+str(ecartTyp)+" "+ '\n')
    else:
        for note in l[1:]:
            note=note.replace(',','.')
            note=float(note)
            ecartType=0
        sortie2.write(nom[2:-2]+" "+str(note)+" "+str(ecartType) + '\n')
    


sortie2.close()


   




