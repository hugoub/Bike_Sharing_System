import modules.GenerateRobustLocDemands as LocDemands
import modules.GenerateStochDist as StochDist
import modules.GenerateStochPonds as StochPonds
import modules.StochMulti as StochMulti
import modules.RobustMulti as RobustMulti
#import modules.PrintVisuals as PrintVisuals
import modules.ReadData as ReadData

#Read Data

demData,locData,A,Aloc = ReadData.ReadData()

#Obtain demand data with Robust Optimization

for i in range(1,6):
    '''
    GenRLocDem(MaxDist,Pondnumber,CategLimits,variation,randomval,outputname,demData,locData,A)
    '''

    # retorna json de 615 pares de Min y Max (RobustLocDemandi.json)

    LocDemands.GenRLocDem(300,1000,[[0.05,1],[0.05,1],[0,0.3],[0.05,0.8]],i,100,'RobustLocDemand' + str(i) + '.json',demData,locData,A)

#Obtain demand data with Stochastic Demands

# json con dict con 1295 keys con 2 lists de length 3, una Pond y otra Cant (StochPondDict.json)

StochDist.GenStoDist(1000,3,[[0.05,1],[0.05,1],[0,0.3],[0.05,0.8]],0,'StochPondDict.json',demData)
'''
GenStoDist(Pondnumber,Scenarios,CategLimits,randomval,outputname,demData):
'''

for i in range(1,6):
    '''
    GenStoPonds(Scenarios,variation,outputname,randomval,demData,PondStochDictFilename)
    '''
    # json con list con 1295 lists de 9 valores entre 0 y 1 cada uno

    StochPonds.GenStoPonds(9,i,'StochPonds' + str(i) + '.json',40,demData,'StochPondDict.json')









#Obtain 5 Solutions for both cases

for i in range(1,6):
    '''
    StochMultiExport(Pvalue,MaxDist,pop_size,max_gen,mutationrate,PondStochDictFilename,PondStochCasesFilename,OutputFilename,randomval,demData,locData,A,Aloc)
    '''
    StochMulti.StochMultiExport(40,300,400,200,0.1,'StochPondDict.json','StochPonds' + str(i) + '.json','StochSols20' + str(i) + '.json',100,demData,locData,A,Aloc)

    '''
    Archivos devueltos
    StochSols20i.json: 
    all_fronts_StochSols20i.json:
    fun_agg_StochSols20i.json:

    '''

for i in range(1,6):
    '''
    RobustMultiExport(Pvalue,MaxDist,pop_size,max_gen,mutationrate,RobustPondsFilename,OutputFilename,randomval,demData,locData,A,Aloc)
    '''
    RobustMulti.RobustMultiExport(40,300,400,200,0.1,'RobustLocDemand' + str(i) + '.json','RobustSols20' + str(i) + '.json',100,demData,locData,A,Aloc)

#Print Results
PrintVisuals.printVis(['StochSols' + str(i) + '.json' for i in range(1,6)])
PrintVisuals.printVis(['RobustSols' + str(i) + '.json' for i in range(1,6)])

'''
StochSols = json.load(open('Results/' + 'StochSols4.json'))
'''