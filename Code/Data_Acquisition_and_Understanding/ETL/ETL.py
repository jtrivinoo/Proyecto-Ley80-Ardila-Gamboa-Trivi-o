#%%
# -*- coding: utf-8 -*-
__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

try:
    ''' Librerías estandar de Python '''
    import os, sys
    from pathlib import Path as p
    import pandas as pd
    
except Exception as exc:
    print('Module(s) ',str(exc), ' are missing.:')

''' Directorio codigo '''
dir_root = p(__file__).parents[0]
sys.path.append(str(p(dir_root) /'source' / 'clases'))
sys.path.append(str(p(dir_root) /'source' / 'utilidades'))


''' Conjunto de utilidades '''
import set_utilidades as ut

''' Clases personalizadas '''
from cls_carga_datos import carga_data
from cls_transforma_datos import transforma_data


''' Clase para vdidaciones '''
from cls_validaciones import valida_data

''' Directorio proyecto'''
dir_root_proy = p(__file__).parents[3]

'''Directorio Raw '''
print(dir_root_proy)
#%%
''' Crear instancias de las clases '''

path_pdf = str(p(dir_root_proy) /'Sample_Data' / 'Raw' / 'Normograma')
lpdf = carga_data(path = path_pdf, u = ut)
lpdf.tipo_archivo = 'pdf'


path_text= str(p(dir_root_proy) /'Sample_Data' / 'Processed'/ 'Normogramatxt')
os.makedirs(path_text, exist_ok=True)
ltxt = carga_data(path = path_text,u = ut)
ltxt.tipo_archivo = 'txt'

path_norm= str(p(dir_root_proy) /'Sample_Data' / 'Processed' / 'procesadoCSV')
os.makedirs(path_norm, exist_ok=True)
lcsv = carga_data(path = path_norm,u = ut)
lcsv.tipo_archivo = 'csv'


path_conc = str(p(dir_root_proy) /'Sample_Data' / 'For_Modeling')
os.makedirs(path_conc, exist_ok=True)
ljson = carga_data(path = path_conc,u = ut)
ljson.tipo_archivo = 'json'

td = transforma_data(path = dir_root_proy,u = ut)
tdpdf = transforma_data(path = path_pdf, u = ut)

vd = valida_data(u = ut)



def get_instancias():
    instancias = {'lcsv':lcsv,
                  'ltxt':ltxt,
                  'lpdf':lpdf,
                  'ljson':ljson, 
                  'td':td,
                  'tdpdf':tdpdf,
                  'vd':vd,
                  }
    
    return instancias

print(path_pdf)

#%%

def listar_archivos_pdf():
    try:
        lpdf.crear_lista_de_archivos(mostrar_lista = True)
        vd.estado = True
    except:
        vd.estado = False
        
        
def listar_carpetas():
    try:
        ltxt.crear_lista_de_carpetas(mostrar_lista = True)
        vd.estado = True
    except:
        vd.estado = False
        
        
def Recopilacion():
    '''
     Alistamiento de datos
        -1 Garantizar la existencia del normograma
        -2 Convertir archivos pdf de normas a texto
        -3 Crear archivo por cada artículo de norma y alojarlo en su carpeta correspondiente 
         
         NOTA: vdidar que cada uno de los pasos se ejecute correctamente.
               donde correctamente equivde a  estado TRUE.
    '''

    print("Inicio Proceso Recopilación")
    
    ''' Paso 1 '''
    '''Garantizar la existencia del normograma (Carpeta PC local)'''
    lpdf.validar_path()
    if lpdf.estado:
        ltxt.path= str(p(dir_root_proy) /'Sample_Data' / 'Processed'/ 'Normogramatxt')
        path_text = p(ltxt.path)
            
        if len(lpdf.lista_de_archivos) > 0:
            for i in range(len(lpdf.lista_de_archivos)):
                ruta_archivo = lpdf.lista_de_archivos[i]
                lpdf.carga_data_en_memoria(ruta_archivo)
                '''Garantizar que los datos se puedan cargar en memoria'''
                if lpdf.estado:
                    file = os.path.splitext(os.path.basename(ruta_archivo))[0]
                    filet = str(file+'.txt')            
                    filepath =str(p(path_text/filet))
                    filepath = p(filepath)  
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    ''' Paso 2 '''
                    '''Convertir archivos pdf de normas a texto'''
                    tdpdf.data = lpdf.data
                    tdpdf.pdf_a_texto(filepath)
                    
                    if tdpdf.estado:
                        ntxtpath =str(p(path_text/file))
                        ntxtpath = p(ntxtpath)  
                        os.makedirs(ntxtpath, exist_ok=True)
                        ''' Paso 3 '''
                        '''Crear archivo por cada artículo de norma y alojarlo en su carpeta correspondiente'''
                        keyword = "ARTÍCULO"
                        tdpdf.separa_texto(ntxtpath, keyword)
                    else:
                         print('Archivo Norma ', ruta_archivo ,' no cargo se tranformo exitosamente a texto')
                         return
                else:
                     print('Archivo Norma ', ruta_archivo ,' no cargo en memoria')
                     return
        else:
             print('Ruta norma ', ruta_archivo ,' no contiene archivos PDF')
    
    print("Fin Proceso Recopilación")
    

def Extraccion(indice = 0):
    '''
     Extracción de datos | Carga datos en memoría:
         -1 Garanztizar la existencia de Carperta de archivos de textos por normas (PC local).
         -2 Garanztizar la existencia de archivos por cada norma (PC local).
         -3 Garantizar que los datos se puedan cargar en memoria.
         -4 Garantizar que el dataframe por norma no contenga filas vacias.
         
         NOTA: vdidar que cada uno de los pasos se ejecute correctamente.
               donde correctamente equivde a  estado TRUE.
    '''
    
    print('Inicio Proceso Extracción ', lpdf.lista_de_archivos[indice])

    path_norm = p(lcsv.path)   
   
    ''' Paso 1 '''
    '''Garanztizar Carperta de archivos de textos por normas (PC local)'''
    ltxt.validar_path()
    if ltxt.estado:
        path_data = str(p(path_text) / ltxt.lista_de_carpetas[indice])
        print(path_data)
        #time.sleep(3)
        ltxt.path = path_data
        ltxt.crear_lista_de_archivos(mostrar_lista = True)
        articulo_num = []
        articulo_cont = []
        
        ''' Paso 2 '''
        '''Garanztizar la existencia de archivos por cada norma (PC local)'''
        if len(ltxt.lista_de_archivos) > 0:
            for i in range(len(ltxt.lista_de_archivos)):
                ruta_archivo = ltxt.lista_de_archivos[i]
                ''' Cargar datos en memoria '''
                ltxt.carga_data_en_memoria(ruta_archivo)
                
                ''' Paso 3 '''
                '''Garantizar que los datos se puedan cargar en memoria'''
                if ltxt.estado:
                    child = os.path.splitext(os.path.basename(ruta_archivo))[0]
                    articulo_num.append(child)
                    articulo_cont.append(ltxt.data)
                else:
                     print('Archivo Articulo ', ruta_archivo ,' no cargo en memoria')
                     continue
                
            columnas = {'No_Articulo' : articulo_num, 'Contenido_Articulo' : articulo_cont}
            
            file = str(ltxt.lista_de_carpetas[indice]+".csv")
            filepath =str(p(path_norm/file))
            
            ltxt.alimentar_df(columnas, filepath)
            if ltxt.estado:
                
                ''' Paso 6 '''
                '''Garantizar que el datframe por norma no contenga filas vacias'''
                vd.data = ltxt.data
                vd.ds_is_empty()
                if not vd.estado:
                   print('Dataframe norma ',path_data, ' vacio')
        else:
             print('Ruta norma ',path_data, ' no contiene archivos')
    
    print('Fin Proceso Extracción ', lpdf.lista_de_archivos[indice])




def Transformacion(indice = 0):
    '''
     Transformación de datos:
         -> Garanztizar la existencia de Carperta de archivos de textos por normas (PC local).
         -> Garantizar que los datos se puedan cargar en memoria.
         -> Validar existencia de datos nulos.       
         -> Validar existencia de datos duplicados.  
         
         Transformaciones generales
             -1 Transformar tipo de dato de ser necesario por columna.
             -2 limpiar campos columnas.
             -3 Agregar columna por nombre norma.
             -4 Guardar archivo por norma transformado.
             -5 Unir archivos transfomados en uno solo.
             -6 Serializar los datos a json
             
        Transformaciones específicas (NLP)
             -> Tokenizar archivo resultado.
             -> Wordcloud archivo resultado.
         
         NOTA: vdidar que cada uno de los pasos se ejecute correctamente.
               donde correctamente equivde a  estado TRUE.
    '''
    print('Inicio Proceso Transformación ',lpdf.lista_de_archivos[indice])
    
    if vd.estado:        
        
        '''Garanztizar la existencia de Carperta de archivos de textos por normas (PC local)'''
        lcsv.validar_path()
        if lcsv.estado:
            lcsv.crear_lista_de_archivos(mostrar_lista = True)
            ruta_archivo = lcsv.lista_de_archivos[indice]
            lcsv.separador = '|'
            lcsv.carga_data_en_memoria(ruta_archivo)
        
        '''Garantizar que los datos se puedan cargar en memoria.'''
        if lcsv.estado:
            vd.data = lcsv.data.copy()
            vd.ds_is_empty()
        else:
            print('carga datos Dataframe ', ruta_archivo, ' no exitoso')
            return
        
        '''Validar existencia de datos nulos'''
        if vd.estado:
            vd.validacion_nulos()
        else:
            print('el Dataframe ', ruta_archivo, ' esta vacio')
            return
        
        '''Validar existencia de datos duplicados'''
        if  vd.estado:
            vd.validacion_duplicados()
        else:
            print('el Dataframe ', ruta_archivo, ' posee datos nulos')
            vd.validacion_duplicados()
            
        if not vd.estado:
            print('el Dataframe ', ruta_archivo, ' posee datos duplicados')
            vd.estado = True        

        if  vd.estado:
            print(os.linesep,' ',lcsv.data.info())            
        
        ''' Transferir los datos a la clase que realiza las transformaciones '''
        td.data = lcsv.data.copy()
        td.path = ruta_archivo
        
        ''' Valida datos en memoría '''
        vd.data = td.data
        vd.ds_is_empty()
        
        ''' Paso 1 '''
        '''Transformar tipo de dato de ser necesario por columna'''
        if  vd.estado:
            string =['No_Articulo', 'Contenido_Articulo']
            td.cambia_tipo_columna(None, None, string)
        else:
            print('el Dataframe ',td.path,' esta vacio')
            return
        
        ''' Paso 2 '''
        '''limpiar campos columnas'''
        if td.estado:
            col = td.data.columns
            for i in range (1,len(col)):
                if td.estado:
                    columna_art = col[i]
                    td.limpia_descripcion(columna_art)
                else:
                    break
        else:
            print('cambio de tipo de datos no exitoso ',td.path)
          
        ''' Paso 3 '''   
        '''Agregar columna por nombre norma'''
        columna = 'Norma'
        if td.estado:
            td.agregar_columna(td.path, columna)
        else:
            print('Limpiar columnas no exitoso ',td.path)    
        
        ''' Paso 4 '''
        '''Guardar archivo por norma transformado.'''
        
        if td.estado:        
            r=os.path.split(td.path)
            file = r[1]
            file = str('transformado_'+file)
            path_tra= str(p(dir_root_proy) /'Sample_Data' / 'Processed'/ 'transformado')
            path_tra = p(path_tra)
            os.makedirs(path_tra, exist_ok=True)
            filepath =str(p(path_tra/file))
            filepath = p(filepath)  
            filepath.parent.mkdir(parents=True, exist_ok=True)
            ut.save(td.data, filepath, 'csv')        
        else:
            print('encotrar polaridad no exitosa ',td.path)
        
        if not td.estado:
            print('Guardar Archivo no exitoso ',td.path)
      
        '''Concatenar Archivos'''
        if td.estado:            
            path_conc= str(p(ljson.path))
            path_conc = p(path_conc)
            
            file = str('procesado_normas.csv')
            filepath =str(p(path_conc/file))
            filepath = p(filepath)
            
            
            if indice == 0:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                procesado_normas = td.data
                columnas = ['Unnamed: 0']                
                td.eliminar_columnas(columnas)
            else:                
                lcsv.separador = '|'
                lcsv.carga_data_en_memoria(filepath)
                procesado_normas = lcsv.data
                procesado_normas = pd.concat([procesado_normas, td.data], axis=0)
                temporal = td.data
                td.data = procesado_normas
                columnas = ['Unnamed: 0']                
                td.eliminar_columnas(columnas)
                colu = td.data.columns
                if 'Unnamed: 0.1' in colu:
                    columnas = ['Unnamed: 0.1']
                    td.eliminar_columnas(columnas)
                procesado_normas = td.data
                td.data = temporal
                    
            '''Generar dataframe concatenado'''        
            
            ut.save(procesado_normas, filepath, 'csv')
            
        else:
            print('el archivo no se guardo exitosamente ',td.path)
            return 
         
        '''Tokenizar archivo resultado'''    
        if td.estado:
            if indice ==(len(lpdf.lista_de_archivos)-1):
                text = procesado_normas['Contenido_Articulo'].astype("string")
                td.tokenizer(text)
            
        else:
            print('el archivo no se concateno exitosamente ',td.path)
            return
        
            
                 
    ''' Paso 6 '''
    '''Serializa los datos a json'''
    
    if td.estado:
                   
        '''Archivo json'''
        r=os.path.split(td.path)
        filej= str(r[1])
        filej= filej.split('.')[0]
        file = str(filej+'.json')        
        path_json= str(p(dir_root_proy) /'Sample_Data' / 'Processed' / 'norma_json')
        path_json = p(path_json)
        os.makedirs(path_json, exist_ok=True)
        filepath =str(p(path_json/file))
        filepath = p(filepath)  
        filepath.parent.mkdir(parents=True, exist_ok=True)        
        
        colu = td.data.columns
                    
        if 'Unnamed: 0' in colu:
            td.data = td.data.rename({'Unnamed: 0': 'index'}, axis=1)
        
        ut.save(td.data, filepath, 'json')
        vd.path = filepath
        vd.validar_path()
        if vd.estado:
            td.estado = True
        else:
            td.estado = False
            print('serializacion Json no exitoso ',td.path)

    else:
        print('Wordcloud no se genero exitosamente')
        return
    
    '''convertir archivo final a json'''
    if td.estado:
       
        if indice ==(len(lpdf.lista_de_archivos)-1):
              path_conc= str(p(dir_root_proy) /'Sample_Data' / 'For_Modeling')
              path_conc = p(path_conc)                
             
              file = str('procesado_normas.csv')
              filepath =str(p(path_conc/file))
              filepath = p(filepath)                               
                      
              lcsv.separador = '|'
              lcsv.carga_data_en_memoria(filepath)
              procesado_normas = lcsv.data
             
              file = str('procesado_normas.json')
              filepath =str(p(path_conc/file))
              filepath = p(filepath)           
              filepath.parent.mkdir(parents=True, exist_ok=True)       
             
              colu = procesado_normas.columns
                         
              if 'Unnamed: 0' in colu:
                  procesado_normas = procesado_normas.rename({'Unnamed: 0': 'index'}, axis=1)
                     
              '''Generar json'''        
         
              ut.save(procesado_normas, filepath, 'json')
              vd.path = filepath
              vd.validar_path()
              if vd.estado:
                  '''Cargar json concatenado Mongo'''
                  ljson.carga_data_en_memoria(filepath)
                  
              else:
                  print('Generar Json concatenado no exitoso {}')
                  return
             
            
    else:
        print('convertir normas a Json no fue exitoso')
        return


def Eliminar_Archivos_Sobrantes(indice = 0):
    '''Eliminar Archivos Sobrantes'''
        
    ''' Directorio proyecto'''
    dir_root_proy = p(__file__).parents[3]

    path_text= str(p(dir_root_proy) /'Sample_Data' / 'Processed'/ 'Normogramatxt')
    path_norm= str(p(dir_root_proy) /'Sample_Data' / 'Processed' / 'procesadoCSV')
    path_tra= str(p(dir_root_proy) /'Sample_Data' / 'Processed'/ 'transformado')
    
    '''Eliminar Normogramatxt'''
    td.rem_dir(path_text)
    print('Borrar archivos', path_text)
    
    if td.estado:            
        '''Eliminar procesadoCSV'''
        td.rem_dir(path_norm)  
        print('Borrar archivos', path_norm)

    
    if td.estado:            
        '''Eliminar transformado'''
        td.rem_dir(path_tra)    
        print('Borrar archivos', path_tra)

    
    if td.estado:            
        '''Eliminar concatenado csv'''
        path_conc= str(p(dir_root_proy) /'Sample_Data' / 'For_Modeling')
        path_conc = p(path_conc)                
    
        file = str('procesado_normas.csv')
        filepath =str(p(path_conc/file))
        filepath = p(filepath)          
    
        td.rem_file(filepath)
        print('Borrar archivos', filepath)