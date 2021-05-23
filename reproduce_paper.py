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

num_sol = 2

for i in range(1,num_sol):
    '''
    GenRLocDem(MaxDist,Pondnumber,CategLimits,variation,randomval,outputname,demData,locData,A)
    '''
    # retorna json de 615 pares de Min y Max (RobustLocDemandi.json)
    LocDemands.GenRLocDem(300,1000,[[0.05,1],[0.05,1],[0,0.3],[0.05,0.8]],i,100,'RobustLocDemand' + str(i) + '.json',demData,locData,A)


for i in range(1,num_sol):
    '''
    RobustMultiExport(Pvalue,MaxDist,pop_size,max_gen,mutationrate,RobustPondsFilename,OutputFilename,randomval,demData,locData,A,Aloc)
    '''
    RobustMulti.RobustMultiExport(20,300,400,200,0.1,'RobustLocDemand' + str(i) + '.json','RobustSols20' + str(i) + '.json',100,demData,locData,A,Aloc)

