# -*- coding: utf-8 -*-
#%%
__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

import os, sys
from pathlib import Path as p
from pprint import pprint


dir_root = p(__file__).parents[0]

ruta_source = str(p(dir_root) /'ETL')

sys.path.append(ruta_source)
import ETL

etl = ETL.get_instancias()


lcsv = etl['lcsv'] 
lpdf = etl['lpdf']
ljson = etl['ljson'] 
td = etl['td']
tdpdf = etl['tdpdf']
vd = etl['vd']
ltxt = etl['ltxt'] 


#%%
def pipeline():
    ETL.listar_archivos_pdf()
    ETL.Recopilacion()
    ETL.listar_carpetas() 
    for indice,_ in enumerate(lpdf.lista_de_archivos):
        print(indice)
        ETL.Extraccion(indice = indice) if vd.estado is True else 'Datos no disponible en memoría.'
        ETL.Transformacion(indice = indice) if vd.estado is True else 'Datos no disponible en memoría.'           

#%%
pipeline()
print(os.linesep,' Archivos procesados:')
pprint(lcsv.summary)

#%%
'''Eliminar Archivos Sobrantes'''
ETL.Eliminar_Archivos_Sobrantes()