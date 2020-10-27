import pandas as pd
import numpy as np
import math
import random
import pickle
import json

#DATA
##MaxDist = 300
##Pondnumber = 1000
##CategLimits = [[0.05,1],[0.05,1],[0,0.3],[0.05,0.8]]
##randomval = 100

def GenRLocDem(MaxDist,Pondnumber,CategLimits,variation,randomval,outputname,demData,locData,A):
    """Generate a file which have de min and max demand for every 
    bike station alternative point
    
    Args:
        MaxDist (int): Maximum Distance among demand points and location alternatives.
        Pondnumber (int): Number for ponderation. 1000.
        CategLimits (list): Limits for every category.
        variation (int): i for for bucle.
        randomval (int): Random seed.
        outputname (str): Output file name.
        demData (dataframe): Points of demand data.
        locData (dataframe):  Location point data.
        A (list): Distance between location points and points of demand.

    Returns:
        --

    Note:
        It generates a file (json) with 615 pairs of Mmin and max demand.
        It named RobustLocDemandI.json with I from 1 to 5.
    """

    #FILE READ
    demLen = len(demData['X'])
    locLen = len(locData['X'])

    #CODE
    random.seed(randomval)
    locdem = dict()

    for j in range(demLen):
        """
        Para cada punto de demanda se busca la estación más cercana
        y se asigna este punto a esta estación.
        locdem tiene como key la estación y como value, los puntos más
        cercanos a esta.
        """
        locmin = -1
        locmindist = 100000
        for i in range(locLen):
            # Va de 615 en 615. 
            if (A[j*locLen+i][1] <= MaxDist and A[j*locLen+i][1] <= locmindist):
                locmin = i
                locmindist = A[j*locLen+i][1]
        if(locmin > -1):
            if(locmin not in locdem):
                locdem[locmin] = []
            locdem[locmin] = locdem[locmin] + [j]

    def RandVals():
        """
        Return a list of 4 values that sum 1.
        """
        randind = [0,1] + [random.random() for i in range(3)]
        randind = sorted(randind)

        randvals = []
        for i in range(len(randind)-1):
            randvals = randvals + [randind[i+1]-randind[i]]

        return randvals

    def demand(i, j):
        return demData['HOUSES'][i]*PondList[j][0]+demData['SHOPS'][i]*PondList[j][1]+demData['EDUCATION'][i]*PondList[j][2]+demData['BUS_STOPS'][i]*PondList[j][3]

    PondList = []
    random.seed(randomval + variation)

    while(len(PondList) < Pondnumber):
        pondsec = RandVals()
        if(pondsec[0] > CategLimits[0][0] and pondsec[0] < CategLimits[0][1]
                and pondsec[1] > CategLimits[1][0] and pondsec[1] < CategLimits[1][1]
                and pondsec[2] > CategLimits[2][0] and pondsec[2] < CategLimits[2][1]
                and pondsec[3] > CategLimits[3][0] and pondsec[3] < CategLimits[3][1]):
            PondList += [pondsec]

    PondDict = dict()
    for i in range(locLen):
        if (i in locdem):
            allpond = [sum([demand(dem,j) for dem in locdem[i]]) for j in range(Pondnumber)]
            PondDict[i] = {'Min': min(allpond),'Max': max(allpond)}
        else:
            PondDict[i] = {'Min': 0,'Max': 0}

    with open('Results/' + outputname, 'w') as fp:
        json.dump(PondDict, fp)
