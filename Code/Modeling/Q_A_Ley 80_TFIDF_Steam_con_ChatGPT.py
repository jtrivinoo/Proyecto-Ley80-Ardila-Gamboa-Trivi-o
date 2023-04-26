# Q&A Ley 80 TFIDF Steam con ChatGPT

__author__ = "Andres Ardila, Johan Triviño, Jenny Gamboa"
__maintainer__ = "Proyecto de Profundización"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
nltk.download("stopwords")
from nltk.stem import SnowballStemmer
import pandas as pd
import openai
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
from pathlib import Path as p
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer


dir_root = p(__file__).parents[2]
print(dir_root)

ruta_source = str(p(dir_root) /'Sample_Data'/'For_Modeling'/'procesado_normas.json')
print(ruta_source)

# LLamado del archivo csv del normograma.
Norma=pd.read_json(ruta_source, encoding='utf-8-sig')
print(Norma.shape)

#Limpieza de columnas que no influyen en el análisis
Norma.drop(['index'], axis = 'columns', inplace=True)

#Definir el idioma de las stopwords en español
stopwords = set(stopwords.words('spanish'))

#Copia del dataframe original. 
Norma1=Norma.copy()


#Función para la aplicación del steaming al corpus del texto. 
def steamer(Corpus):        
  Corpus=[i.lower() for i in Corpus]
  stem=SnowballStemmer('spanish')  
  Corpus=[' '.join([stem.stem(j) for j in i.split()]) for i in Corpus]
  return Corpus

#Ciclo con la funcion de guardar las normas en minúscula, en una lista.
Norma2 = []
for j,i in enumerate(Norma1["Contenido_Articulo"]):
    if type(i)==str:
        Norma2.append(i.lower())

#Ciclo para agregar una columna al dataframe con el steaming aplicado. 
for i in range (len(Norma1['Contenido_Articulo'])):
  Norma1['Contenido_Articulo'][i] =pd.Series(Norma1['Contenido_Articulo'][i])
  Corpus= steamer(Norma1['Contenido_Articulo'][i])
  Norma1['Contenido_Articulo'][i]= Corpus[0]  

#Ciclo para formar una lista de la norma sin stopwords y en minúscula. 
Normasinparada=[]
for i,noti in enumerate(Norma2):
    Normasinparada.append([j.lower() for j in noti.split() if not j.lower() in stopwords and len(j)>1])

Normasinparada2=[' '.join(i) for i in Normasinparada]

#Aplicación de vectorización por el metodo Tfidf
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(Normasinparada2)
y = vectorizer.transform(Normasinparada2)

#Distancia Euclidiana
distancias_y = euclidean_distances(X,y)

#Agregar columna con el contenido sin steam. 
Norma1['Contenido_Articulo_Completo']=Norma['Contenido_Articulo']

#Retorno de Dataframe de contexto
def procesar_pregunta(pregunta):
    global Norma
    global Norma1
    global X
    y=vectorizer.transform([pregunta])
    distancias_y=cosine_distances(X,y)  
    ind=np.argsort(distancias_y,axis=0).reshape(Norma.shape[0])[:20]
    Nor = Norma1[['Norma','No_Articulo','Contenido_Articulo_Completo']].loc[ind]
    df = Nor.copy()
    df.loc[len(df)] = ['', '', '']
    return df

#Retorno de aticulos relacionados
def Articulos_relacionados(df):    
    df1 = df[['Norma','No_Articulo']].head(20)
    return df1


# Credenciales de OpenAI
#openai.api_key = "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"
openai.api_key = "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"
# Carga el contexto


# Estilo de la tabla
estilo_tabla = {
    'max-width': '100px',
    'margin': 'auto',
    'font-family': 'Arial',
    'border': '1px solid black',
    'border-collapse': 'collapse',
    'text-align': 'right',
}

estilo_encabezado = {
    'font-size': '18px',
    'background-color': 'lightgrey',
    'font-weight': 'bold',
    'padding': '5px',
    'textAlign': 'center'
}

estilo_celda = {
    'padding': '5px',
}

estilo_titulo = {
    'text-align': 'center',
}

# Inicializa la aplicación Dash
app = dash.Dash(__name__)

# Define la interfaz de usuario
app.layout = html.Div([
    html.H1("QA Contratación Pública Colombia", style=estilo_titulo),
    html.Div([
        dcc.Textarea(
            id="texto",
            placeholder="Escribe tu pregunta aquí...",
            style={"width": "100%", "height": 100}
        ),
        html.Button("Enviar", id="boton"),
    ]),
    html.Div(id="respuesta")    
])

# Define la función para hacer la pregunta a OpenAI
respuestas_dadas =[]
def hacer_pregunta(contexto, pregunta, respuestas_dadas):
    prompt = f"{contexto}  Pregunta: {pregunta} Respuesta:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    for choice in response.choices:
        if "Respuesta:" in choice.text:
            nueva_respuesta = choice.text.replace("Respuesta:", "").strip()
            if nueva_respuesta not in respuestas_dadas:
                respuestas_dadas.append(nueva_respuesta)
                return nueva_respuesta, respuestas_dadas
            else:
                return None, respuestas_dadas
        break
    return None, respuestas_dadas

# Define la función que se ejecuta al hacer clic en el botón
@app.callback(
    Output('respuesta', 'children'),
    [Input('boton', 'n_clicks')],
    [State('texto', 'value')]
)
def actualizar_respuesta(n_clicks, pregunta):
    global respuestas_dadas
    if pregunta:
        df = procesar_pregunta(pregunta)
        df1 =Articulos_relacionados(df)
        for i, row in df.iterrows():
            contexto = row["Contenido_Articulo_Completo"]
            print(len(contexto))
            respuesta, respuestas_dadas_nueva = hacer_pregunta(contexto, pregunta, respuestas_dadas)
            if respuesta:
                # Genera un resumen con ChatGPT
                resumen = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Resumen del texto: {pregunta}  Para contratación pública en Colombia En Español",
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                # Obtiene la respuesta del resumen generado por ChatGPT
                for choice in resumen.choices:
                    if "Resumen del texto:" not in choice.text:
                        resumen_generado = choice.text.strip()
                        break
                # Muestra el resumen y la respuesta
                respuesta_split = respuesta.split('Pregunta:')
                primeros_tres = " ".join(respuesta_split[:2])
                #print(respuesta_split)
                respuestas_dadas = respuestas_dadas_nueva # actualiza la variable global
                return html.Div([                
                    html.P(resumen_generado, style={'font-weight': 'bold'}),
                    html.P(primeros_tres, style={'color': 'Black'}),
                    html.Div([
                            html.H2("Artículos relacionados", style=estilo_titulo),
                            dash_table.DataTable(
                                id='tabla',
                                columns=[{"name": i, "id": i} for i in df1.columns],
                                data=df1.to_dict('records'),
                                style_cell=estilo_celda,
                                style_header=estilo_encabezado,
                                style_table=estilo_tabla,
                            )
                        ], style={'width': '100%', 'float': 'right'})
                ])                
            else:
                respuestas_dadas = respuestas_dadas_nueva # actualiza la variable global
                continue # pasa al siguiente row
        return html.P("No se encontró ninguna respuesta.", style={'color': 'red'})

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
