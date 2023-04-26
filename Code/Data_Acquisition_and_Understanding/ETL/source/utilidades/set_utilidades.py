# -*- coding: utf-8 -*-
__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"


try:
    import os
    import sweetviz
    from pathlib import Path as p
    
except Exception as exc:
    print('Module(s)', str(exc),' are missing.:')



        
def describe_data_en_memoria(data):
    '''
    Presenta la descripción general del conjunto de datos. Asimismo, para las variables 
    numéricas presenta los principales estadísticos descriptivos.
    
    Parameters
    ----------
    data : dataframe
        DESCRIPTION. dataframe al que se le realizara la descripción

    Returns
    -------
    None.

    '''
    try:
        data.describe()
        
    except Exception as exc:
       mostrar_error(exc)


    
def lista_variables_por_tipo(data):
    '''
    Genera una lista por cada uno de los tipos de variables contenidas en el dataframe
    contenido en el atributo data de la clase.

    Parameters
    ----------
    data : dataframe
        DESCRIPTION. dataframe al que se le generara la lista de tipo de variables

    Returns
    -------
    varT : TYPE
        DESCRIPTION.

    '''
    try:
        varT = []             
        varD = data.dtypes.tolist()
        varD = set(varD)
        varD = list(varD)
                   
        for n in range(len(varD)):
            Dtype = data.select_dtypes(include = varD[n]).columns
            Dtype = Dtype.tolist()
            Dtype = {str(varD[n]) : Dtype}
            varT.append(Dtype)
                       
        return varT
            
    except Exception as exc:
        mostrar_error(exc)
    
 
           
def muestra_data_en_pantalla(data, numero_filas = None):
    '''
    La función debe mostrar la cantidad de filas requeridas o el total de filas cuando
    no reciba el parámetro numero_filas.

    Parameters
    ----------
    data : dataframe
        DESCRIPTION. dataframe que se mostrara los datos en pantalla
    numero_filas : string, optional
        DESCRIPTION. The default is None.
        numero de filas a mostrar

    Returns
    -------
    None.

    '''
    try:
        print(data[0:numero_filas])
        
    except Exception as exc:
        mostrar_error(exc)
    

    
def muestra_archivos(lst_files):
    '''
    Imprime en pantalla cada uno de los elementos contenidos en lst_files.

    Parameters
    ----------
    lst_files : list
        DESCRIPTION. lista de archivos a mostrar

    Returns
    -------
    None.

    '''
    try:
        for count, f in enumerate(lst_files):
            child = os.path.splitext(os.path.basename(f))[0]
            print('\t',count,child)
            
    except Exception as exc:
        mostrar_error(exc)
        


def save(data, filename = None, tipo = None):
    '''
    Agregar la opción para guardar datos en diferentes formatos como son csv y json

    Parameters
    ----------
    data : dataframe
        DESCRIPTION. datframe a guardar en archivo
    filename : string, optional
        DESCRIPTION. The default is None.
        nombre de archivo a gurardar
    tipo : string, optional
        DESCRIPTION. The default is None.
        tipo de archivo a guardar

    Returns
    -------
    None.

    '''
    try:
        if filename is not None and tipo is not None:
            
            if tipo == 'xlsx':
                data.to_excel(filename , sheet_name = 'sheet', index=False)
                
            elif tipo == 'csv':
                data.to_csv(filename, encoding='utf-8-sig', sep = '|')
            
            elif tipo == 'parquet':
                data.to_parquet(filename)
            
            elif tipo == 'json':
                data.to_json(filename, orient = 'records') 
            
            else:
                print('tipo de archivo ', tipo,' no valido para guardado')
        else:
            print('tipo de archivo no valido para guardado')
        
    except Exception as exc:
        mostrar_error(exc)
        

        
def mostrar_error(ex):
    '''
    Captura el tipo de error, su description y localización.

    Parameters
    ----------
    ex : Object
        Exception generada por el sistema.

    Returns
    -------
    None.

    '''
    
    trace = []
    tb = ex.__traceback__
    while tb is not None:
        trace.append({
                      "filename": tb.tb_frame.f_code.co_filename,
                      "name": tb.tb_frame.f_code.co_name,
                      "lineno": tb.tb_lineno
                      })
        
        tb = tb.tb_next
        
    print(os.linesep,' Something went wrong:')
    print('---Exception: ',ex,os.linesep)
    print('---type: ',str(type(ex).__name__))
    print('---message: ', str(type(ex)))
    print('---trace: ',str(trace))

def profiling(path, data, ruta_archivo):
    '''
    Crear perfil de los datos para posterior analisis

    Parameters
    ----------
    path : string
        DESCRIPTION. ruta de archivo donde se guardara el EDA
    data : dataframe
        DESCRIPTION. dataframe al que se le realizara el EDA
    ruta_archivo : string
        DESCRIPTION. ruta de dataframe que se le realizara el EDA

    Returns
    -------
    None.

    '''
    try:
        name_eda = 'EDA_' + str(os.path.splitext(os.path.basename(ruta_archivo))[0]) + '.html'
        path_eda = str(p(path) /'output' / name_eda)
        path_eda = p(path_eda)
        path_eda.parent.mkdir(parents=True, exist_ok=True)
            
        my_report = sweetviz.analyze(data)
        my_report.show_html(path_eda)

    except Exception as exc:
        mostrar_error(exc)
    







