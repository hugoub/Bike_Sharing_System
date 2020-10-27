import pandas as pd
import numpy as np
import math
import random
import pickle
import json

#DATA
##Pondnumber = 1000
##Scenarios = 3
##CategLimits = [[0.05,1],[0.05,1],[0,0.3],[0.05,0.8]]
##randomval = 0

def GenStoDist(Pondnumber,Scenarios,CategLimits,randomval,outputname,demData):
    """ Function that generate a low, medium and high demand 
    per demand point and the probability that each happens.

    Args:
        Pondnumber (int): Number of demands to estimate.
        Scenarios (int): Number of divisions of the demands.
        CategLimits (list): List of inferior and superior limits for each category.
        randomval (int): Seed for random module
        outputname (str): Random name
        demData (list): Data of demand points.

    Returns:
        --

    Note:
        Generate a dict with 1295 elements for every demand point. Each element 
        with 2 keys, 'Pond' and 'Cant', where Pond are the low, medium and high 
        demand and Cant is every probability.
    
        The file returned is named StochPondDict.json and it is in the results folder.
    """
    demLen = len(demData['X'])
    random.seed(randomval)

    def PointRand(r1,r2):
        """ Return 4 random number and their sum is 1

        Args:
            ---
        """
        randind = [0,1] + [random.random() for i in range(3)]
        randind = sorted(randind)
        randvals = []
        for i in range(len(randind)-1):
            randvals = randvals + [randind[i+1]-randind[i]]
        return randvals

    PondList = []
    while(len(PondList)<Pondnumber):
        pondsec = PointRand(np.random.uniform(),np.random.uniform())
        if(pondsec[0]>CategLimits[0][0] and pondsec[0]<CategLimits[0][1] and pondsec[1]>CategLimits[1][0] and
           pondsec[1]<CategLimits[1][1] and pondsec[2]>CategLimits[2][0] and pondsec[2]<CategLimits[2][1] and
           pondsec[3]>CategLimits[3][0] and pondsec[3]<CategLimits[3][1]):
            PondList += [pondsec]
    # PondList is a list which has 1000 elements with 4 ponderations.
    
    PondDict = {}
    PondEsp = []
    for i in range(demLen):
        # allpond correspond to H, it es the ponderated demand for each point
        allpond = [demData['HOUSES'][i]*PondList[j][0]+demData['SHOPS'][i]*PondList[j][1]+demData['EDUCATION'][i]*PondList[j][2]+demData['BUS_STOPS'][i]*PondList[j][3] for j in range(Pondnumber)]
        
        cantScenarios = [0 for i in range(Scenarios)]
        for j in range(Pondnumber):       
            den = (max(allpond)-min(allpond))
            if den==0:
                den = 1
            x = math.floor((allpond[j]-min(allpond))*Scenarios/den)
            if(x == Scenarios):
                x -= 1
            cantScenarios[x] += 1
        PondDict[i] = {'Pond': [((max(allpond)-min(allpond))/Scenarios)*(j+1/2)+min(allpond) for j in range(Scenarios)],'Cant': [cantScenarios[i]/Pondnumber for i in range(len(cantScenarios))]}
    
    with open('Results/' + outputname, 'w') as fp:
        json.dump(PondDict, fp)


