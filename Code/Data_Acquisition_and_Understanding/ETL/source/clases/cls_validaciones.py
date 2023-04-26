# -*- coding: utf-8 -*-
__author__ = "Roberto Arias"
__maintainer__ = "Asignatura Big Data - Taller OOP in Data Science"
__copyright__ = "Copyright 2022 - Asignatura Big Data"
__version__ = "0.0.1"



try:
    import pandas as pd
    import numpy as np
    from chardet.universaldetector import UniversalDetector
    import os
    
except Exception as exc:
    print('Module(s) ', str(exc),' are missing.:')



class valida_data(object):
    
    
    def __init__(self,u = None):
        self.utils = u
        self.estado = False
        self.d_encode = None
        self.data = None
        self.flag = False
        self.contador = 0
        self.band = False
        self.dimension = None
        self.perdida = None
        self.duplicados = None
        
        
    def ds_is_empty(self):
        '''
        Valida si el contenido de un Dataframe es vacio

        Returns
        -------
        None.

        '''
        
        try:
            if self.data.empty is not True:
                self.estado = True
            else:
                self.estado = False
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def validar_path(self):
       '''
        Valida que exista el path desde dónde se está tratando de cargar los datos. En caso que el path
        no exista, se debe terminar el proceso y reportar el error.

        Returns
        -------
        None.

        '''
        
       try:
           
          if  self.path is not None and os.path.exists(self.path):
              self.estado = True
          else:
              self.estado = False
        
        
              
       except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
    
            
    def valida_encode_archivo(self, path, flag):
        '''
        Valida que el tipo de codificacion de los archivos primer intento con Chardet segundo intento con lista de ecoding

        Parameters
        ----------
        path : string
            DESCRIPTION. ruta de archivo a validar encode
        flag : bool
            DESCRIPTION. bandera para comprobar estado

        Returns
        -------
        None.

        '''  
        try:
            
            if not flag:                   
                filename = path
                detector = UniversalDetector()
                for line in open(filename, 'rb'):
                    detector.feed(line)
                    if detector.done: break
                detector.close()
                
                self.d_encode =detector.result['encoding']
                self.flag = True
                self.estado = True
                
            else:
                encodings = ['windows-1250', 'windows-1251','windows-1252', 'gb2312', 'ISO-2022-JP', 'iso-8859-1', 'cp949']
                Le= len(encodings)
                if self.contador < Le:
                    self.d_encode = encodings[self.contador]
                    self.contador +=1
                    self.estado = True
                    
                else:
                    self.band = True
                    self.estado = False
                    
        
        except Exception as exc:
            #self.estado = False
            self.utils.mostrar_error(exc) 
            
            
    def validacion_dimensiones(self):
        '''
        Validar las dimensiones de la tabla para saber si cargo información correctamente, a pesar de leer bien el 
        Dataframe

        Returns
        -------
        None.

        '''           
        try:
            self.dimension = self.data.shape
            dimension = self.dimension
            
            if dimension[0] == 0:
                self.estado = False
            else:
                self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
                
    def validacion_columnas(self):
        '''
        Validar cantidad de Columnas adecuadas de acuerdo a la informacion de kaggle.

        Returns
        -------
        None.

        '''
        try:
            
            columnas = self.data.columns
            lc = len(columnas)
            
            if lc != 16:                        
               self.estado = False 
            else:                             
                self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
    
    def validacion_nulos(self):
        '''
        Validar cantidad de datos con id nulos contenido en el dataframe.

        Returns
        -------
        None.

        '''
        try:
            self.validacion_dimensiones()
            dimension = self.dimension
            if self.estado:
                self.perdida= self.data.isnull().sum()
                porcentajeN = 100*self.perdida.sum()/np.product(dimension)
                if porcentajeN > 0:
                    self.estado = False
                else:
                    self.estado = True             
                                        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def validacion_duplicados(self):
        '''
        Validar cantidad de datos duplicados.

        Returns
        -------
        None.

        '''
        try:
            self.duplicados = self.data[self.data.duplicated()]
            if self.duplicados.empty is not True:
                self.estado = False
            else:            
                self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
           
        
    
    