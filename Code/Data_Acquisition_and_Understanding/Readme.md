# This folder hosts code for data acquisition and understanding (exploratory analysis)

EN
This data acquisition project is based on an object-oriented programming project in python developed with the Spyder IDE.

In a brief description, it runs through a pipeline that loads an ETL script, which uses various classes, validation scripts, and utilities. that are in charge of extracting, transforming and saving the data that will be used for modeling at its final destination.

This project consists of the following folders and files:

Pipeline: "\Azure-TDSP-ProjectTemplate-master\Code\Data_Acquisition_and_Understanding\FlujoDeDatos.py"
This file Executes the entire ETL data flow.

Parent folder: "\Azure-TDSP-ProjectTemplate-master\Code\Data_Acquisition_and_Understanding\ETL"

    ETL.py file: This file contains all the execution steps of the ETL.
    File LEEME.txt: This file contains indications about the libraries needed to run and the data flow.

    Sub forlders:
        "~\ETL\Log":
            Files: 
                log.txt: This file contains all the execution logs of the project.  
        
        "~\ETL\source":
            Sub forlders:
                "~\source\clases":
                    Files: 
                        cls_carga_datos.py: This class contains instances that allow the loading and selection of data types in a way that suits the needs of the data flow.
                        cls_transforma_datos.py: This class contains instances that allow you to perform the necessary transformations to make the data ready for modeling.
                        cls_validaciones.py: This class contains instances that allow you to perform validations that allow you to monitor the flow of data.
                
                "~\source\utilidades":
                    Files:
                        set_utilidades.py: This script contains useful functions for the execution of data flow.




SP
Este proyecto de adquisición de datos se basa en un proyecto de programación orientada a objetos en python desarrollado con el IDE de Spyder.

En una breve descripción, se ejecuta a través de un Pipeline que carga un script ETL, que utiliza varias clases, scripts de validación y utilidades. que se encargan de extraer, transformar y guardar los datos que serán utilizados para el modelado en su destino final.

Este proyecto se compone de las siguientes carpetas y archivos:

Pipeline: "\Azure-TDSP-ProjectTemplate-master\Code\Data_Acquisition_and_Understanding\FlujoDeDatos.py"
Este archivo Ejecuta todo el flujo de datos de la ETL.

Carpeta principal: "\Azure-TDSP-ProjectTemplate-master\Code\Data_Acquisition_and_Understanding\ETL"

    Archivo ETL.py: Este archivo contiene todos los pasos de ejecución del ETL.
    Archivo LEEME.txt: Este archivo contiene indicaciones sobre las librerías necesarias para ejecutar y el flujo de datos.

    Sub carpetas:
        "~\ETL\Log":
            Archivos: 
                log.txt: Este archivo contiene todos los logs de ejecucion del proyecto.
    
        "~\ETL\source":
            Sub Carpetas:
                "~\source\clases":
                    Archivos: 
                        cls_carga_datos.py: Esta clase contiene instancias que permiten, la carga y seleccion de tipos de datos de manera que se ajuste a las necesidades del flujo de datos.
                        cls_transforma_datos.py: Esta clase contiene instancias que permiten realizar las transformaciones necesarias para que los datos estén listos para el modelado.
                        cls_validaciones.py: Esta clase contiene instancias que permiten realizar validaciones que permiten monitorear el flujo de datos.
                
                "~\source\utilidades":
                    Archivos:
                        set_utilidades.py: Este script contiene funciones útiles para la ejecución del flujo de datos.
