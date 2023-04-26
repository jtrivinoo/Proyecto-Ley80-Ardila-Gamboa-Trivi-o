# -*- coding: utf-8 -*-
__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"



try:
    import pandas as pd
    from datetime import datetime
    from matplotlib.image import imread 
    from urllib import request as req
    import os
    import shutil
    from pathlib import Path as p
    import nltk
    from spacy.lang.es.stop_words import STOP_WORDS
    STOP_WORDS_S = STOP_WORDS
    from nltk.corpus import stopwords
    nltk.download("stopwords")
    import re
    
    
    
except Exception as exc:
    print('Module(s) ',str(exc),' are missing.:')



class transforma_data(object):
    
    
    def __init__(self, u = None, path=None):
        self.utils = u
        self.path = path
        self.estado = False
        self.data = None
        # Agregar los atributos de clase que consideren necesarios.
        
        
    def eliminar_columnas(self, columnas):
        '''
        Se eliminan las columnas que no se consideran necesarias despues del analisis EDA

        Parameters
        ----------
        columnas : list
            DESCRIPTION. nombre colunas a eliminar.

        Returns
        -------
        None.

        '''        
        try:
            
            self.data = self.data.drop(columnas, axis = 'columns')            
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def eliminar_duplicados(self, columnas):
        '''
        Se eliminan duplicados de acuerdo a una lista de columnas para consideración

        Parameters
        ----------
        columnas : list
            DESCRIPTION. nombre columnas que determinan duplicados.

        Returns
        -------
        None.

        '''        
        try:
            self.data = self.data.drop_duplicates(subset = columnas, keep="first")
                        
            duplicados= self.data[self.data.duplicated()].shape[0]
            if duplicados == 0:                                    
                self.estado = True
            else:
                self.estado = False
           
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
     
        
    def cambia_tipo_columna(self, enteros=None, tiempo= None, string = None):
        '''
        A partir de varias listas se cambia el tipo de dato de Columna

        Parameters
        ----------
        enteros : list, optional
            DESCRIPTION. The default is None.
            lista de variables  que corresponde a tipo enteros
        tiempo : list, optional
            DESCRIPTION. The default is None.
            lista de variables  que corresponde a tipo time
        string : list, optional
            DESCRIPTION. The default is None.
            lista de variables  que corresponde a tipo string

        Returns
        -------
        None.

        '''        
        try:
            tc= self.utils.lista_variables_por_tipo(self.data)
            enteros64 = []
            enteros32 = []
            strings = []
            tiempos = []

            for i in range (len(tc)): 
                tci = tc[i]
                ktci = list(tci.keys())
                ktci = ktci[0]
                if ktci  == 'int64':
                    enteros64 = tci[ktci]
                elif ktci  == 'int32':
                    enteros32 = tci[ktci]
                elif ktci  == 'str':
                    strings = tci[ktci]
                elif ktci  == 'time':
                    tiempos = tci[ktci]
                    
            if enteros is not None:
                for i in range (len(enteros)):
                    if len(enteros32) > 0 or len(enteros64) > 0:
                        if enteros[i] not in enteros32 and enteros[i] not in enteros64:
                            enteros[i] = int(enteros[i])
                            self.data[enteros[i]] = self.data[enteros[i]].astype('int32')
                    else:
                        self.data[enteros[i]] = self.data[enteros[i]].astype('int32')
            
            if tiempo is not None:        
                for i in range (len(tiempo)):
                    self.data[tiempo[i]] = self.data[tiempo[i]].astype("string")
                    self.data[tiempo[i]] = self.data[tiempo[i]].str.replace(".", "/")
                    d_parse = lambda x : datetime.strptime(x, "%y/%d/%m")
                    if len(tiempos) > 0:
                        if tiempo[i] not in tiempos:            
                           self.data[tiempo[i]] = self.data[tiempo[i]].apply(d_parse)
                    else:
                        self.data[tiempo[i]] = self.data[tiempo[i]].apply(d_parse)
                    
            if string is not None:                  
                for i in range (len(string)):
                    if len(strings) > 0:
                        if string[i] not in strings:
                            self.data[string[i]] = self.data[string[i]].astype("string")
                    else:
                        self.data[string[i]] = self.data[string[i]].astype("string")
                    

            self.data.info()                       
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    
    def cruzar_json(self, dataj, citems, colcat, nid, nsnip, ntitle):
        '''
        A partir de varias listas se cambia el tipo de dato de Columna

        Parameters
        ----------
        dataj : dict
            DESCRIPTION. dataset json
        citems : string
            DESCRIPTION. nombre de la clave dataset json
        colcat : string
            DESCRIPTION. columna datset csv
        nid : string
            DESCRIPTION. nombre columna id
        nsnip : string
            DESCRIPTION. nombre de la clave snip dataset json
        ntitle : string
            DESCRIPTION. nombre de la clave titulo dataset json

        Returns
        -------
        None.

        '''
        try:
            items = dataj.get(citems)
            lim = len(items)            
            self.data[colcat] = self.data[colcat].astype("string")
            for contador in range(lim):
                items_dict = items[contador]
                ids = items_dict.get(nid)
                titles = items_dict.get(nsnip)
                titulo = titles.get(ntitle) 
                ids= str(ids)
                titulo = str(titulo)
                self.data[colcat] = self.data[colcat].str.replace('^'+ids+'$', titulo, regex=True)
            
           
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
   
    def miniaturas(self, path_thumb, url_column, nombre_thumb):
        '''
        Descargar las miniaturas por video y gaurdarlas en una columna especifica

        Parameters
        ----------
        path_thumb : string
            DESCRIPTION. ruta donde se guardara la miniatura
        url_column : string
            DESCRIPTION. nombre de la columna donde esta la url de la miniatura
        nombre_thumb : string
            DESCRIPTION. nombre que se le asignara a la miniatura descargada

        Returns
        -------
        None.

        '''
        try:
            
            folder = path_thumb
            for the_file in os.listdir(folder): 
                file_path = os.path.join(folder, the_file)                
                if os.path.isfile(file_path): 
                    os.unlink(file_path) 
            
            rango =len(self.data[url_column])            
            
            col = self.data.columns            
            if 'thumbnail_matrix' not in col:
                self.data['thumbnail_matrix'] = ''
            self.data.info()

            
            for i in range (rango):
                try:       
                    url = self.data[url_column].values[i]
                    fname = self.data[nombre_thumb].values[i]
                    pfile = str(p(path_thumb)/fname)
                    pfile = str(pfile+'.jpg')
                    req.urlretrieve(url, pfile)
                except:
                    self.data.loc[i, 'thumbnail_matrix'] = str("thumbnail Not found")
                else:
                    imageToMatrice  = imread(pfile)
                    self.data.loc[i, 'thumbnail_matrix'] = str(imageToMatrice)
                    
                
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def agrupar_tags(self, column, filepath):
        '''
        Crea un archivo auxiliar que contenga el conteo de los tags por país.

        Parameters
        ----------
        column : string
            DESCRIPTION. nombre de la columna donde se extraen los tags
        filepath : string
            DESCRIPTION. ruta donde se guardara el dataset de tags tipo csv

        Returns
        -------
        None.

        '''
        try:
            
            rango =len(self.data[column])
            ltags =[]
            for i in range (rango):
                tags_cell = self.data[column].values[i]
                ls_tcell = tags_cell.split('|')
                
                for j in range (len(ls_tcell)):
                    ltags.append(ls_tcell[j])                
            
            
            dftags = pd.DataFrame({column : ltags})

            group_tags = dftags.groupby([column])[column].count()
                
            filepath = p(filepath)  
            filepath.parent.mkdir(parents=True, exist_ok=True)  
            self.utils.save(group_tags, filepath, 'csv')
            
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
    
               
            
    def limpia_descripcion(self, columna):
        '''
        Limpiar campo description

        Parameters
        ----------
        columna : string
            DESCRIPTION. nombre columna a limpiar

        Returns
        -------
        None.

        '''
        try:
            self.data[columna] = self.data[columna].str.replace('(?![[:ascii:]]+)', '', regex=True)  
            self.data[columna] = self.data[columna].str.replace('\-|\*|\@|\#|\°|\|', '', regex=True) 
            self.data[columna] = self.data[columna].str.replace('\n\s*\n', '\n', regex=True)  
           
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
             
    
    def agregar_columna(self, ruta, columna):
        '''
        Agrega columna tipo string llena con nombre del archivo

        Parameters
        ----------
        ruta : string 
            DESCRIPTION. ruta del archivo de la cual se extraera el contenido de columna
        columna : string
            DESCRIPTION. nombre de la columna a agregar

        Returns
        -------
        None.

        '''
        try:
            pass
            col = self.data.columns
    
            child = os.path.splitext(os.path.basename(ruta))[0]
                
            if columna not in col:
                self.data[columna] = child
                self.data[columna] = self.data[columna].astype("string")
            self.data.info()
                    
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    
    def pdf_a_texto(self, filepath):
        '''
        Convertir los datos leidos de un archivo pdf a un archivo texto

        Parameters
        ----------
        filepath : string
            DESCRIPTION. ruta donde se tomara el archivo pdf

        Returns
        -------
        None.

        '''
        try:            
            self.data = self.data.encode('utf-8-sig','replace')
            self.data = str(self.data.decode('utf-8-sig'))
            self.data = re.sub(u'\ufb01', 'fi', self.data)
            self.data = re.sub(u'\ufb02', 'fl', self.data)
            self.data = re.sub(u'[\ufb00-\ufbff]', '', self.data)
            self.data = self.data.split(sep='\n')
            with open(filepath, 'w', encoding='utf-8-sig') as filehandle:
                for element in self.data:
                    element = re.sub(r'\n\s*\n', '\n', element).strip()
                    if element != '':
                        filehandle.write(element + "\n")                    
                        self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def separa_texto(self, folderpath, keyword):
        '''
        A partir de una lista y una palabara clave (en mayuscula), generarl archivos separados

        Parameters
        ----------
        folderpath : string
            DESCRIPTION. ruta donde se tomaran los archivo a guardar
        keyword : string
            DESCRIPTION. palabra clave por la cual se separara el contenido del archivo

        Returns
        -------
        None.

        '''
        try:            
            dl = self.data
            dart= []
            counter = 1
            artaux = ''
            flag= False
            #filepath =''
            for element in dl:
                element = re.sub(r'\n\s*\n', '\n', element).strip()
                element = element.replace('    ', ' ')
                element = element.replace('   ', ' ')
                element = element.replace('  ', ' ')
                element = element.replace('\n', ' ')
                lup = element.upper()
                pos = lup.find(keyword)
                #print(element)
                              
                if element =='' or element ==' ':
                    continue
                
                if pos == 0:
                    spl = element.split(" ")
                    #print(len(spl))
                    if len(spl) > 1:
                        art = str(spl[0]+' '+spl[1])                        
                    else:
                        continue
                    
                    art = str(art)
                    reg = re.search("^A.+\d{1}", art)
                    
                    if "Artículos" in spl[0]:
                        dart.append(element)
                        flag = False
                        continue
                    
                    if flag:
                        flag = False
                        dart.append(element)                        
                  
                    elif reg != None:
                        
                        if  len(spl)>=4 and("artículo" in spl[3] or "artículo" in spl[4] or "Adiciónese" in spl[2] or "Modifíquese" in spl[2] or "Modifíquese el Artículo" in element  or "Adiciónese el Artículo" in element or "quedara así" in element):
                            flag = True
                            #print("split --------", spl[3])
                            
                        
                        if counter != 1:
                          #print("Este es el articulo --------", art)
                          file = str(artaux+'.txt')                          
                          artaux =art  
                          
                        else:
                            #print("Este es el articulo --------", art)
                            file = str('Introduccion.txt')
                            artaux =art
                            
                            
                        filepath =str(p(folderpath / file))
                        filepath = p(filepath)
                        filepath.parent.mkdir(parents=True, exist_ok=True)
                        with open(filepath, 'w') as filehandle:
                            for item in dart:
                                item.strip()
                                if item != '':
                                    filehandle.write(item + " ")
                        filehandle.close()
                        counter +=1
                        dart = [element]
                    else:
                        dart.append(element)
                else:
                    dart.append(element)
                    
            file = str(artaux+'.txt')
            filepath =str(p(folderpath / file))
            filepath = p(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)        
            with open(filepath, 'w') as filehandle:
                for item in dart:
                    item.strip()
                    if item != '':
                        filehandle.write(item + " ")
            filehandle.close()       
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    
    def my_tokenizer(self, text):
        '''
        Realiza proceso de tokenización

        Parameters
        ----------
        text : list|string
            DESCRIPTION. lista de stringa a tokenizar

        Returns
        -------
        list
            DESCRIPTION. lista de string tokenizado

        '''
        try:
            return text.split() if text != None else []
            self.estado = True
            
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    
    def remove_stopwords(self, tokens):
        '''
        Detecta Stop Words libreria spacy

        Parameters
        ----------
        tokens : list|string
            DESCRIPTION. lista de palabras a la que se dectaran palabras que no aportan valor

        Returns
        -------
        list
            DESCRIPTION. lista de palabras que no aportan valor

        '''
        try:
            from spacy.lang.es.stop_words import STOP_WORDS
            STOP_WORDS_S = STOP_WORDS
            return [t for t in tokens if t not in STOP_WORDS_S]
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            

    def remove_stopwords1(self, tokens):
        '''
        Detecta Stop Words libreria nltk

        Parameters
        ----------
        tokens : list|string
            DESCRIPTION. lista de palabras a la que se dectaran palabras que no aportan valor

        Returns
        -------
        list
            DESCRIPTION. lista de palabras que no aportan valor

        '''
        try:            
            stopword_es = nltk.corpus.stopwords.words('spanish') 
            return [t for t in tokens if t not in stopword_es]
            self.estado = True
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
    def tokenizer(self, text):
        '''
        Realiza proceso de tokenización mostrando cantidad de palabara tokenizadas, removidas y resultado

        Parameters
        ----------
        text : list|string
            DESCRIPTION. texto al que se le removera las palabra que no aportan valor

        Returns
        -------
        list
            DESCRIPTION. resultado de palabra a las que se le removio las palabra que no aportan valor

        '''
        try:            
            texto =''
            for i in text:
                texto= texto+i
    
            print("cantidad de palabras y/o frases al tokenizar")
            print(len(self.my_tokenizer(texto)))
    
            text_split = self.my_tokenizer(texto)
            
            print("cantidad de palabras que no aportan significado")
            print( len(self.remove_stopwords(self.remove_stopwords1(texto))))
    
            print("cantidad de palabras y/o frases luego de remover stopwords")
            texto_rem = self.remove_stopwords(self.remove_stopwords1(text_split))
            
            print(len(texto_rem))
            
            self.estado = True
        
        except Exception as exc:
            self.estado = False
            self.utils.mostrar_error(exc)
            
        
    def dict_to_df(self, columnas):
        '''
        A partir de un diccionario devuelve un dataframe de 2 columnas

        Parameters
        ----------
        columnas : dict
            DESCRIPTION. diccionario del cual se tomara el contenido del dataframe

        Returns
        -------
        None.

        '''
        try:
            lkey = list(self.data.keys())
            lvalue = list(self.data.values())
            
            dfdict = pd.DataFrame({columnas[0] : lkey, columnas[1]: lvalue})
            self.data =dfdict
            self.estado = True
         
        except Exception as exc:
             self.estado = False
             self.utils.mostrar_error(exc)
    
    def rem_file(self, ruta):
        '''
        A partir de un diccionario devuelve un dataframe de 2 columnas

        Parameters
        ----------
        columnas : dict
            DESCRIPTION. diccionario del cual se tomara el contenido del dataframe

        Returns
        -------
        None.

        '''
        try:
            os.remove(ruta)
            self.estado = True
         
        except Exception as exc:
             self.estado = False
             self.utils.mostrar_error(exc)
             
    def rem_dir(self, ruta):
        '''
        A partir de un diccionario devuelve un dataframe de 2 columnas

        Parameters
        ----------
        columnas : dict
            DESCRIPTION. diccionario del cual se tomara el contenido del dataframe

        Returns
        -------
        None.

        '''
        try:            
            shutil.rmtree(ruta)
            self.estado = True
         
        except Exception as exc:
             self.estado = False
             self.utils.mostrar_error(exc)
             
    
             
    