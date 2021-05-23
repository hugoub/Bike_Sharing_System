import pandas as pd
import numpy as np
import math
import random
import pickle
import json

#DATA
##randomval = 100
##Pvalue = 40
##MaxDist = 300
##pop_size = 400
##max_gen = 200
##mutationrate = 0.1
##RobustPondsFilename='RobustLocDemands1.json'
##OutputFilename='RobustSols.json'

def RobustMultiExport(Pvalue,MaxDist,pop_size,max_gen,mutationrate,RobustPondsFilename,OutputFilename,randomval,demData,locData,A,Aloc):

    #FILE READ
##    demData = pd.read_excel('Data/Demands.xlsx')
##    locData = pd.read_excel('Data/Locations.xlsx')
##    A = pickle.load(open("Data/dist.p","rb"))
##    Aloc = pickle.load(open("Data/dist_among_location.p","rb"))
    RobustPonds = json.load(open('Results/' + RobustPondsFilename))

    #CODE
    random.seed(randomval)
    locLen = len(locData['X'])
    demLen = len(demData['X'])

    totLen = locLen+demLen

    ABool = [[1 if A[j*locLen+i][1] <= MaxDist else 0 for i in range(locLen)] for j in range(demLen)]

    solution = [random.sample(range(locLen), Pvalue) for i in range(pop_size)]

    def functionRobust(pop):
        robustdemands = [RobustPonds[str(i)]['Min'] if i in pop else RobustPonds[str(i)]['Max'] for i in range(locLen)]
        fitness = sum(sorted(robustdemands, reverse=True)[:Pvalue]) - sum([robustdemands[i] for i in pop])
        return -fitness

    def functionStoch(pop):
        fitness = 0
        covered = set([j for j in range(demLen) for i in pop if ABool[j][i]==1])
        return sum([PondStochDict[str(i)]['Pond'][PondStochCases[i][w]]*PondStochDict[str(i)]['Cant'][PondStochCases[i][w]] for i in covered for w in range(scenarios)])

    def functionLocDist(pop):
        fitness = 9999999999
        for i in pop:
            for j in pop:
                if(i!=j and Aloc[j*locLen+i][1] < fitness):
                    fitness = Aloc[j*locLen+i][1]
        return fitness

    def crossover(a,b):
        popoptions = list(set(a) | set(b))
        pop = random.sample(popoptions, Pvalue)
        return pop

    def mutation(a):
        pop = random.sample(a, Pvalue-1)
        popoptions = [i for i in range(locLen) if i not in pop]
        pop = pop + random.sample(popoptions, 1)
        return pop

    def fast_non_dominated_sort(values1, values2):
        S=[[] for i in range(0,len(values1))]
        front = [[]]
        n=[0 for i in range(0,len(values1))]
        rank = [0 for i in range(0, len(values1))]

        for p in range(0,len(values1)):
            S[p]=[]
            n[p]=0
            for q in range(0, len(values1)):
                if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                    if q not in S[p]:
                        S[p].append(q)
                elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                    n[p] = n[p] + 1
            if n[p]==0:
                rank[p] = 0
                if p not in front[0]:
                    front[0].append(p)

        i = 0
        while(front[i] != []):
            Q=[]
            for p in front[i]:
                for q in S[p]:
                    n[q] = n[q] - 1
                    if(n[q]==0):
                        rank[q]=i+1
                        if q not in Q:
                            Q.append(q)
            i = i+1
            front.append(Q)

        del front[len(front)-1]
        return front


    def crowding_distance(values1, values2, front):
        distance = [0 for i in range(0,len(front))]
        sorted1 = sort_by_values(front, values1[:])
        sorted2 = sort_by_values(front, values2[:])
        distance[0] = 4444444444444444
        distance[len(front) - 1] = 4444444444444444
        for k in range(1,len(front)-1):
            distance[k] = distance[k]+ (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
        for k in range(1,len(front)-1):
            distance[k] = distance[k]+ (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
        return distance

    def sort_by_values(list1, values):
        sorted_list = []
        while(len(sorted_list)!=len(list1)):
            if index_of(min(values),values) in list1:
                sorted_list.append(index_of(min(values),values))
            values[index_of(min(values),values)] = math.inf
        return sorted_list

    def index_of(a,list):
        for i in range(0,len(list)):
            if list[i] == a:
                return i
        return -1

    val_fun1 = {}
    val_fun2 = {}
    front_elements = {}

    gen_no=0
    while(gen_no<max_gen):
        print('Robust Generation = ', gen_no)
        function1_values = [functionRobust(solution[i])for i in range(0,pop_size)]
        function2_values = [functionLocDist(solution[i])for i in range(0,pop_size)]
        val_fun1[gen_no] = function1_values
        val_fun2[gen_no] = function2_values
        non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:])
        front_elements[gen_no] = non_dominated_sorted_solution
##        print("The best front for Generation number ",gen_no, " is")
##        for valuez in non_dominated_sorted_solution[0]:
##            print(solution[valuez],end=" ")
##        print("\n")
        crowding_distance_values=[]
        for i in range(0,len(non_dominated_sorted_solution)):
            crowding_distance_values.append(crowding_distance(function1_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
        solution2 = solution[:]
        #Generating offsprings
        while(len(solution2)!=2*pop_size):
            a1 = random.randint(0,pop_size-1)
            b1 = random.randint(0,pop_size-1)
            solution2.append(crossover(solution[a1],solution[b1]))
        for i in range(len(solution2)):
            if(random.random() < mutationrate):
                solution2[i] = mutation(solution2[i])
        function1_values2 = [functionRobust(solution2[i])for i in range(0,2*pop_size)]
        function2_values2 = [functionLocDist(solution2[i])for i in range(0,2*pop_size)]
        non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:],function2_values2[:])
        crowding_distance_values2=[]
        for i in range(0,len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(crowding_distance(function1_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
        new_solution= []
        for i in range(0,len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front.reverse()
            for value in front:
                new_solution.append(value)
                if(len(new_solution)==pop_size):
                    break
            if (len(new_solution) == pop_size):
                break
        solution = [solution2[i] for i in new_solution]
        gen_no = gen_no + 1


    function1_values = [functionRobust(solution[i])for i in range(0,pop_size)]
    function2_values = [functionLocDist(solution[i])for i in range(0,pop_size)]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:])


    SolRobust = {}
    SolID = 1
    for valuez in non_dominated_sorted_solution[0]:
        Solutions = pd.DataFrame({'X': [], 'Y': [], 'ID':[]})
        for i in solution[valuez]:
            Solutions = Solutions.append({'X': locData['X'][i], 'Y': locData['Y'][i], 'ID': i}, ignore_index=True)
        covered = set([j2 for j2 in range(demLen) for i2 in solution[valuez] if ABool[j2][i2]==1])

        SolRobust[SolID] = {'IDs': [int(i) for i in Solutions['ID']], 'Covered': list(covered), 'Objective': round(functionRobust(solution[valuez]),10), 'MinDist': round(functionLocDist(solution[valuez]),3)}
        SolID = SolID + 1

    val_fun1[gen_no] = function1_values
    val_fun2[gen_no] = function2_values
    front_elements[gen_no] = non_dominated_sorted_solution

    with open('Results/' + OutputFilename, 'w') as fp:
        json.dump(SolRobust, fp)

    fun_agg = {'f1':val_fun1, 'f2':val_fun2}
    with open('Results/fun_agg_' + OutputFilename, 'w') as fp:
        json.dump(fun_agg, fp)

    with open('Results/all_fronts_' + OutputFilename, 'w') as fp:
        json.dump(front_elements, fp)
    