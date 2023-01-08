import os
import torch
import torch.nn as nn
import numpy as np
from torchvision.io import read_image
import pandas as pd
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from nltk.tokenize import word_tokenize

#réseau neurone 2 couches cachée 512 neurones
#f act : relu, batch size 64 pour le gros fichier svm train
#softmax : proba 10 classes
#pytorch tuto prof cours traitement auto langue naturel
#classe dataset gere données sous forme vecteur
#fichier svm sous forme vecteur : entrée réseau de neurone
#classifieur SVM : vecteur de taille fixe en entrée

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.linear1 = nn.Linear(2000000, 512)
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(512, 512)
        self.relu2 = nn.ReLU()
        self.linear3 = nn.Linear(512, 10)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu1(x)
        x = self.linear2(x)
        x = self.relu2(x)
        x = self.linear3(x)
        x = self.softmax(x)
        return x

svm_file_train="train_Extrait.svm"
svm_file_test="test_Extrait.svm"

class CustomImageDataset(Dataset):
    def __init__(self, svm_file_train):
        self.counter=0
        fp=open(svm_file_train, 'r')
        line=fp.readlines()
        self.counter = len(line)
        fp.close()
            
    #len : nb com corpus
    def __len__(self):
        return self.counter

    #retourne vecteur idx
    def __getitem__(self, idx):
        cpt=0
        
        with open(svm_file_train, 'r') as fp:
            vec = [0] * 2000000
            lines = fp.readlines()
            # fermez le fichier après avoir lu les lignes
            fp.close()
            # Itérer sur les lignes
            index=[]
            occurence=[]
            linesAvecNote=[]
            linesSansNote=[]
            cpt=0
            for line in lines:
                if cpt==idx:
                    lineSplit=line.split()
                    linesAvecNote=lineSplit[0]
                    linesSansNote=lineSplit[1:]
                    
                    for lines in linesSansNote:
                        indexOccurence=lines.split(':')
                        index.append(indexOccurence[0])
                        occurence.append(indexOccurence[1])
            
                cpt=cpt+1            
            
            index = list(map(int, index))
            occurence = list(map(int, occurence))  

            for i in range(len(index)):
                vec[index[i]-1]=occurence[i]
            
            #print("note = ", linesAvecNote)
            
            output=[0]*10
            #output[int(linesAvecNote)]=1
            #print(output)
            
            return torch.FloatTensor(vec), torch.FloatTensor(output)
        
training_data = CustomImageDataset(svm_file_train)
train_dataloader = DataLoader(training_data, batch_size=1)
loss_fn = nn.CrossEntropyLoss()

model=NeuralNetwork()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
#print("avant train loop") 
def train_loop(train_dataloader, model, loss_fn, optimizer):
    #print("avant for")
    size = len(train_dataloader)
    #print(size)
    for batch, (X, y) in enumerate(train_dataloader):
        #print("après for")
        
        #print("X= ", X)
        #print("y = ",y)
        # Compute prediction and loss
        pred = model(X)
        #print("pred= ", pred)
        loss = loss_fn(pred, y)
        
        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
        #if batch % 10 == 0:
        loss, current = loss.item(), batch * len(X)
        print(f"loss: {loss:>7f}")
        
for epochs in range(0, 1):
    train_loop(train_dataloader, model, loss_fn, optimizer)
 
print("++++++++++++++++++++++++++++++++++")
   
test_data = CustomImageDataset(svm_file_test)
test_dataloader = DataLoader(test_data, batch_size=1)

for batch, (X, y) in enumerate(test_dataloader):
    print("batch = ",batch)
    #print("X= ", X)
    #print("y = ",y)
    
    # Compute prediction and loss
    pred = model(X)
    print("pred test = ",pred)
    
    #Récupère la note prédite (proba la plus grande)
    y_pred = pred.argmax(dim=1)
    print("y_pred = ", y_pred)
    
    noteFormate=str(y_pred)
    
    print((int(noteFormate[8])+1))
    
