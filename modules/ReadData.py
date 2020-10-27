import pandas as pd
import pickle

def ReadData():
    '''
    Lee los datos desde la carpeta data
    '''
    demData = pd.read_excel('Data/Demands.xlsx')    # Shops / Education / BusStop / X / Y - Son más valores
    locData = pd.read_excel('Data/Locations.xlsx')  # Puntos en el Plano. Los X, Y de arriba
    A = pickle.load(open("Data/dist.p","rb"))       
    Aloc = pickle.load(open("Data/dist_among_location.p","rb")) # Igual al anterior pero con 378.225 valores. 
    demLen = len(demData['X'])  # 1295
    locLen = len(locData['X'])  # 615
    return demData,locData,A,Aloc

'''
import geopandas as gp
df=gp.read_file('C:/Users/rodel/Documents/GitHub/paper_Bikesharing/data/centroids.shp')
df=gp.read_file('C:/Users/rodel/Dropbox/Mauricio Research/ultimosDatos/centroid_casas_comercial_educacion_busstop.shp')
df['X'] = df.geometry.apply(lambda p: p.x)
df['Y'] = df.geometry.apply(lambda p: p.y)
df.rename(columns={'TOTAL_PERS':'HOUSES'}, inplace=True)
df.drop(['REGION', 'PROVINCIA','COMUNA','COD_DIS','COD_ZON','COD_ENT','MANZENT','DES_REGI','DES_PROV','DES_COMU'], axis=1, inplace=True)
df.drop(['REGION', 'PROVINCIA','COMUNA','COD_DIS','COD_ZON','COD_ENT','MANZENT','DES_REGI','DES_PROV','DES_COMU'], axis=1, inplace=True)
df['HOUSES']=df['HOUSES']/df['HOUSES'].sum()
df['SHOPS']=df['SHOPS']/df['SHOPS'].sum()
df['BUS_STOPS']=df['BUS_STOPS']/df['BUS_STOPS'].sum()
df['EDUCATION']=df['EDUCATION']/df['EDUCATION'].sum()
df.to_file(driver = 'ESRI Shapefile', filename= 'C:/Users/rodel/Documents/GitHub/paper_Bikesharing/data/dema.shp')
df.to_excel('C:/Users/rodel/Documents/GitHub/paper_Bikesharing/data/Demands.xlsx') 
'''