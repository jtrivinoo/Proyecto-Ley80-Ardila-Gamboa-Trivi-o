# -*- coding: utf-8 -*-
__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"



try:
    import pandas as pd
    import json
    import glob
    import os
    from pathlib import Path as p
    from pdfminer.high_level import extract_text
    
    
except Exception as exc:
    print('Module(s) ',str(exc),' are missing.:')



class carga_data(object):
    
    
    def __init__(self,u = None, path=None,tipo_archivo=None):
        self.utils = u
        self.tipo_archivo = tipo_archivo
        self.path = path
        self.data = None
        self.lista_de_archivos = None
        self.estado = False
        self.summary = {}
        self.separador = ','
      
        
        
        
        
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
     
        
     
    def valida_tipo_archivo(self,tipo):
        '''
        Valida que el formato del archivo que se está leyenda está dentro de los permitos; en caso
        que no, debe terminar el proceso.
        Los archivo permitidos son: csv, json, y parquet.

        Parameters
        ----------
        tipo : String
            DESCRIPTION. tipo de archivo a validar

        Returns
        -------
        None.

        '''
         
        try:
            
            permitidos = ['.csv', '.json', '.parquet', '.txt', '.pdf']
            if  tipo is not None:
                nombre, extension = os.path.splitext(tipo)
                if  extension is not None and extension in permitidos:
                  self.estado = True
         
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
        

        
    
    def crear_lista_de_archivos(self, mostrar_lista= False):
        '''
        Lista los archivo de un directorio segun el tipo solicitado.

        Parameters
        ----------
        mostrar_lista : bool, optional
            DESCRIPTION. The default is False.
            determina si se muestra en consola la lista de archivos

        Returns
        -------
        None.

        '''
        try:
            
            self.lista_de_archivos = [f for f in glob.glob(str(self.path)+'/**/*.'+ self.tipo_archivo.lower(), recursive=True)]
            
            if mostrar_lista:
                print(os.linesep,' Archivos tipo : ',self.tipo_archivo)
                self.utils.muestra_archivos(self.lista_de_archivos)
                
            self.estado = True
            
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
            
    def crear_lista_de_carpetas(self, mostrar_lista= False):
        '''
        Lista los archivo de un directorio segun el tipo solicitado.

        Parameters
        ----------
        mostrar_lista : bool, optional
            DESCRIPTION. The default is False.
            determina si se muestra en consola la lista de carpetas

        Returns
        -------
        None.

        '''
        try:
         with os.scandir(self.path) as ficheros:
               
              self.lista_de_carpetas = [fichero.name for fichero in ficheros if fichero.is_dir()]
        
             
         if mostrar_lista:
            print('Carpetas Normas:')
            self.utils.muestra_archivos(self.lista_de_carpetas)
                
            self.estado = True
            
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
        
        
    def carga_data_en_memoria(self, the_path):
        '''
        Carga datos desde un archivo y los organiza en un dataframe de pandas
        El dataframe resultante se debe asignar al atributo data de la clase.
        
        Parameters
        ----------
        the_path : String
            DESCRIPTION. ruta del archivo a cargar en memoria.

        Returns
        -------
        None.

        '''

        try:
            # Usar función que valida el tipo de archivo
            self.valida_tipo_archivo(the_path)
            
            #self.estado = True
            child = os.path.splitext(os.path.basename(the_path))[0]
            
            if self.estado:
                if self.tipo_archivo == 'csv':
                    try:
                        self.data = pd.read_csv(the_path,encoding="utf-8", 
                                                sep = self.separador)
                        self.separador = ','
                        self.estado = True
                        self.summary[child] = 'True'
                    except:
                        self.data = pd.read_csv(the_path,encoding="ISO-8859-1", 
                                                sep = self.separador)
                        self.separador = ','
                        self.estado = True
                        self.summary[child] = 'True'
                        
                elif self.tipo_archivo == 'txt':
                    archivo = open(the_path)                 
                    self.data = archivo.read()
                    archivo.close()
                    self.estado = True
                    self.summary[child] = 'True'
                    
                elif self.tipo_archivo == 'json':
                    with open(the_path) as file_json:
                        self.data = json.load(file_json)
                        
                    self.estado = True
                
                elif self.tipo_archivo == 'parquet':
                    self.data = pd.read_parquet(the_path, encoding=(self.d_encode))
                    self.estado = True
                    self.summary[child] = 'True'
                
                elif self.tipo_archivo == 'pdf':
                    contenido = extract_text(the_path, codec='utf-16', laparams=None)

                    # Codificar el contenido utilizando la opción 'replace' para reemplazar los caracteres no válidos
                    contenido_codificado = contenido.encode('utf-8', 'replace')

                    # Decodificar el contenido codificado
                    contenido_decodificado = contenido_codificado.decode('utf-8-sig')
                    self.data = contenido_decodificado 
                                                    
                    self.estado = True
                    self.summary[child] = 'True'
            
                else:
                    print('El tipo de archivo ',self.tipo_archivo,' no es permitido')
                    self.estado = False
                    
                    
            else:
                print('El tipo de archivo ',self.tipo_archivo,' no es permitido')
                self.estado = False
                
        except Exception as exc:
            self.estado = False
            self.summary[child] = 'False'
            self.utils.mostrar_error(exc)
            
    
    
    def selecciona_variables(self, lista_de_variables):
     '''
        selecciona las variables que se van a utilizar dada una lista de variables.
        El proceso debe validar que existan esas variables en el conjunto de datos. En
        caso de no estar presente alguna de las variables, debe reportarlo en pantalla.

        Parameters
        ----------
        lista_de_variables : lista
            DESCRIPTION. lista de variables a validar.

        Returns
        -------
        None.

        '''
     
     try:
         varD = self.data.columns.tolist()
         inter = set(varD) & set(lista_de_variables)
         inter = list(inter)
         self.data = self.data.loc[inter]
         print(lista_de_variables - varD)
     except Exception as exc:
         self.estado = False
         self.utils.mostrar_error(exc)
         
    
    def alimentar_df(self, columnas, filepath):
        '''
        Crea y alimenta un Datframe a partir de un diccionario de columnas
        generando un archivo csv como salida.

        Parameters
        ----------
        columnas : dict
            DESCRIPTION. lista de nombres de columnas del datframe.
        filepath : string
            DESCRIPTION. ruta donde se guardara el archivo.

        Returns
        -------
        None.

        '''        
        try:
            df_arts = pd.DataFrame(columnas)
            
            filepath = p(filepath)  
            filepath.parent.mkdir(parents=True, exist_ok=True)  
            self.utils.save(df_arts, filepath, 'csv')
            self.data= df_arts
            self.estado = True          
            
            
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)

    

