# -*- coding: utf-8 -*-

   
ligneOut=""
nbCom=0
nbfichierOutFormate=0
with open("outUserMoviePolarite01.txt", 'r', encoding='utf8') as fichierIn, open("outFormate.txt", "r") as fichierOutFormate, open("outUserMoviePolarite01Formate.txt", "w") as fichierOutFormateFinal:
    
    #fichierIn: note pas formatté
    for ligne in fichierIn :
        nbCom=nbCom+1
        
        #print("ligne dans note : ",ligne) 
         
        #fichierOutFormate : review id
        for ligne1 in fichierOutFormate :
            #print("ligne1 dans note : ",ligne1) 
            nbfichierOutFormate = nbfichierOutFormate +1
            #print("ligne dans review id : ",ligne+ " "+ligne1) 
            note=str(int(ligne)/2)
            ligneOut=ligne1.replace('\n', '')  + " " + note.replace('.',',')
            #print(note)
            #fichierOutFormateFinal.write(ligne+ " "+str(int(ligne1)/2)+"\n")
            fichierOutFormateFinal.write(ligneOut+"\n")
            
            ligne = fichierIn.readline()
            #ligne1 = fichierOutFormate.readline()
print("___________________________")
print("ligne dans note : ",nbCom) 
print("ligne dans review id : ",nbfichierOutFormate)  

fichierIn.close()
fichierOutFormate.close()
fichierOutFormateFinal.close()
