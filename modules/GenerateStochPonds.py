import pandas as pd
import numpy as np
import math
import pickle
import random
import json

#Data
randomval = 40
Scenarios = 9

#Code
def GenStoPonds(Scenarios,variation,outputname,randomval,demData,PondStochDictFilename):
    """ Generate 5 files. Every one with a list of 1295 demands point
    and every point with 9 scenarios (0, 1 or 2). Shape: (1295, 9).

    Args:
        Scenarios (int): Number of different scenarios per all demand points.
        variation (int): i from for bucle.
        outputname (str): Name of output file.
        randomval (int): Seed for using in random.
        demData (list): Data of demand points.
        PondStochDictFilename (str): File obtained from GenerateStochDist module
            with name StochPondDict.json.

    Returns:
        --

    Note:
        The names of files generated are StochPondsI.json, with I from 1 to 5.
    """
    
    PondStochDict = json.load(open('results/' + PondStochDictFilename))
    demLen = len(demData['X'])

    CaseSelect = [[0 for i in range(Scenarios)] for j in range(demLen)]
    random.seed(a=randomval + variation)
    for i in range(demLen):
        for w in range(Scenarios):
            rand = random.random()
            j=0
            scenval = PondStochDict[str(i)]['Cant'][0]
            while rand > scenval:
                j+=1
                scenval += PondStochDict[str(i)]['Cant'][j]
            CaseSelect[i][w] = j
    with open('Results/' + outputname, 'w') as fp:
        json.dump(CaseSelect, fp)
