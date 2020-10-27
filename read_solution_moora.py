import numpy as np
import ujson
import pandas as pd
import matplotlib.pyplot as plt

num_stations = 20       # 20 y 40

# Part 1. Reading solutions

solutions = []
for i in range(1,6):
    with open("results_" + str(num_stations) + "/StochSols20"+str(i)+".json") as file:
        res_js = file.read()
        solutions.append(ujson.loads(res_js))

for i in range(1,6):
    with open("results_" + str(num_stations) + "/RobustSols20"+str(i)+".json") as file:
        res_js = file.read()
        solutions.append(ujson.loads(res_js))

res_inter = []
obj_1 = []
obj_2 = []

n_sto = 0
for i in range(len(solutions)):
    if i < 5:       
        n_sto = n_sto + len(solutions[i]) 
    for j in solutions[i].keys():
        res_inter.append(sorted(solutions[i][j]['IDs']))
        obj_1.append(solutions[i][j]['Objective'])
        obj_2.append(solutions[i][j]['MinDist'])

n_rob = len(res_inter) - n_sto


plt.plot(sorted(obj_1))


# Part 2. Reading matrix raster

matrix_rango = pd.read_csv('tif_files/matrix_rango.csv', sep=';').to_numpy()
matrix_proximity = pd.read_csv('tif_files/matrix_proximity.csv', sep=';').to_numpy()
locations = pd.read_csv('tif_files/locations_with_id.csv', sep=';').to_numpy()

w_1 = [0.365656566,0.182828283,0.068473223,0.100683272,0.02181193,0.023228319,0.062846371,0.025264488,0.149207549]


w = np.array(w_1).reshape(1,-1)


matrix_rango_pond= np.zeros((len(res_inter),9))
for i in range(len(res_inter)):
    sol = matrix_rango[res_inter[i]][:,1:10] 
    #sol = matrix_proximity[res_inter[i]][:,1:10] 
    matrix_rango_pond[i,:] = np.sum(sol,0,keepdims=True)   # The sum of all stations values in one solution (it could be the average too)
    #matrix_rango_pond[i,:] = np.average(sol, axis=0).reshape(1,-1)     # average


### Librerias de MCDM

from skcriteria import Data, MIN, MAX
import itertools
from skcriteria.madm.moora import norm, rank
from skcriteria.madm.moora import *

mt = Data(matrix_rango_pond, [MAX]*9, weights=w.reshape(-1))  


### Parte 1. Ratio System

matrix_rango_pond_sqr = np.square(matrix_rango_pond)
matrix_rango_pond_den = np.sqrt(np.sum(matrix_rango_pond_sqr, axis = 0, keepdims = True))

matrix = matrix_rango_pond / matrix_rango_pond_den
y = np.sum(matrix * w, axis = 1, keepdims = True)

matrix_df = pd.DataFrame(y)

# El orden_1 esta ordenado de mejor a peor solución
# El ord_1 tiene el valor de ranking que toma cada solucion
# El ord_1_by_lib tiene el valor de ranking que toma cada solucion pero obtenido a traves de la libreria

orden_1 = matrix_df.sort_values(0, ascending = False).index

ord_1 = np.zeros(len(orden_1))
for i in range(len(orden_1)):
    ord_1[orden_1[i]] = i+1


def ratio(nmtx, ncriteria, nweights):

    # invert the minimization criteria
    cweights = nweights * ncriteria

    # calculate raning by inner prodcut
    rank_mtx = np.inner(nmtx, cweights)
    points = np.squeeze(np.asarray(rank_mtx))
    return rank.rankdata(points, reverse=True), points


ord_1_by_lib = ratio(matrix_rango_pond, mt.criteria, mt.weights)
ord_1_by_lib[0]


### Part 1. Reference Point

vector_rango_max = np.max(matrix, axis = 0)

matrix_rango_rf =  vector_rango_max*w - matrix*w

y_ref = np.max(matrix_rango_rf, axis = 1, keepdims=True)

matrix_ref = pd.DataFrame(y_ref)

orden_2 = matrix_ref.sort_values(0, ascending = True).index

ord_2 = np.zeros(len(orden_2))
for i in range(len(orden_2)):
    ord_2[orden_2[i]] = i+1


def refpoint(nmtx, criteria, weights):
    # max and min reference points
    rpmax = np.max(nmtx, axis=0)
    rpmin = np.min(nmtx, axis=0)

    # merge two reference points acoording criteria
    mask = np.where(criteria == MAX, criteria, 0)
    rpoints = np.where(mask, rpmax, rpmin)

    # create rank matrix
    rank_mtx = np.max(np.abs(weights * (nmtx - rpoints)), axis=1)
    points = np.squeeze(np.asarray(rank_mtx))
    return rank.rankdata(points), points

ord_2_by_lib = refpoint(matrix, mt.criteria, mt.weights)
ord_2_by_lib[0]


### Parte 3: Full multiplicative form

y_m = np.prod(matrix_rango_pond, axis = 1, keepdims=True)
matrix_m = pd.DataFrame(y_m)
orden_3 = matrix_m.sort_values(0, ascending = False).index

ord_3 = np.zeros(len(orden_3))
for i in range(len(orden_3)):
    ord_3[orden_3[i]] = i+1

fm = FMFMOORA()
fm_2 = fm.solve(mt)
fm_3 = fm.decide(mt)
fm_3.rank_

'''
### Full multiplicative form según paquete

aa = np.min(np.log(matrix))
bb = np.log(matrix)-aa+1
y_m = np.sum(np.log(matrix)*w, axis = 1, keepdims=True)
matrix_m = pd.DataFrame(y_m)
orden_3 = matrix_m.sort_values(0, ascending = False).index

a = np.zeros(len(orden_3))
for i in range(len(orden_3)):
    a[orden_3[i]] = i+1
'''


'''
rm = RatioMOORA()
rpm = RefPointMOORA()
fm = FMFMOORA()
fm_1 = fm.decide(mt) 
fm_1.best_alternative_  # solo funcionan con decide
fm_1.rank_
'''


'''
# Obtener la solucion directamente con el paquete
# No toma en cuenta los pesos
mm = MultiMOORA()

mm_1 = mm.solve(mt)     # rustico
mm_1 = mm.decide(mt)    # dataframe

mm_1.best_alternative_  # solo funcionan con decide
mm_1.rank_

best_solution = mm_1.best_alternative_
'''

# Parte de MULTIMOORA

ratio_rank = ord_1
refpoint_rank = ord_2
fmf_rank = ord_3

rank_mtx = np.vstack((ratio_rank, refpoint_rank, fmf_rank)).T

alternatives = rank_mtx.shape[0]
points = np.zeros(alternatives)
for idx0, idx1 in itertools.combinations(range(alternatives), 2):
    alt0, alt1 = rank_mtx[idx0], rank_mtx[idx1]
    dom = rank.dominance(alt0, alt1)
    dom_idx = idx0 if dom > 0 else idx1
    points[dom_idx] += 1

rank_mm = rank.rankdata(points, reverse=True)
# rank_mtx      # Los 3 rankings

alternativa = np.array(range(alternatives))[rank_mm<=20].reshape(-1,1)
first_20 = rank_mm[rank_mm<=20].reshape(-1,1)
first_20_2 =rank_mtx[rank_mm<=20]

table = np.concatenate((alternativa, first_20_2, first_20), axis = 1)
table_df = pd.DataFrame(table, dtype=int)
table_df.columns = ['alternativas','ratio','ref','form','multimoora']
table_df = table_df.sort_values('multimoora',ascending=True)
#table_df.to_csv("multi_20.csv",sep=';')

best_solution = np.where(rank_mm == 1)[0][0]

sol_df = pd.DataFrame(locations[res_inter[best_solution]])
sol_df.columns = ['point_id','X','Y']
#sol_df.to_csv("solucion_" + str(num_stations) + ".csv",sep=';')


plt.plot(table_df)



'''
# Pareto de todas las soluciones
res_1 = []
res_2 = []
for i,j in zip(obj_1,obj_2):
    num = 0
    itera = 0
    for k,l in zip(obj_1,obj_2):
        itera += 1
        if (i <= k and j < l) or (i < k and j <= l):
            num =+ 1
        if itera == len(obj_1) and num == 0:
            res_1.append(i)
            res_2.append(j)

# plt.plot(obj_1, obj_2, '.')
# plt.plot(res_1, res_2, '.')
res_inter = np.array(res_inter).reshape(-1)

frec = np.zeros((615))
for j in res_inter:
    frec[j] += 1

frec_sort = np.sort(frec)
'''