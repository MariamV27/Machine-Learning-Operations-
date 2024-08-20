
#Modelo de recomendaciones

import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from scipy.sparse import hstack
from fastapi import FastAPI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors


# Indicamos título y descripción de la API
app = FastAPI(title='Machine-Learning-Operations-',
            description='API de datos y recomendaciones de peliculas')

# Global variables
df_highly_rated = None
cv = None
count_matrix = None
cosine_sim = None
indices = None

@app.on_event("startup")
async def load_data():
    global df_combined,df_highly_rated, cv, count_matrix, nn, indices

    # Carga los datos
    df_highly_rated = pd.read_excel('./Datos_transformados.xlsx')
    df = df_highly_rated

    # Computa la matriz de recuento
    #  cv = CountVectorizer(stop_words='english', max_features=5000)
     # count_matrix = cv.fit_transform(df_highly_rated['combined_features'])

    # Crea un modelo NearestNeighbors
     # nn = NearestNeighbors(metric='cosine', algorithm='brute')
     # nn.fit(count_matrix)

    # Crea un índice de títulos de películas
    indices = pd.Series(df_highly_rated.index, index=df_highly_rated['title']).drop_duplicates()

@app.get('/')
async def read_root():
    return {'Mi primera API. Dirígite a /docs'}

@app.get('/about/')
async def about():
    return {'Proyecto individual Nº1: Recomendacion de peliculas'}

@app.get('/')
async def read_root():
    return {'Mi primera API. Dirígite a /docs'}

@app.get('/about/')
async def about():
    return {'Proyecto individual Nº1: Recomendacion de peliculas'}


##############
@app.get('/')
async def read_root():
    return {'Mi primera API. Dirígite a /docs'}

@app.get('/about/')
async def about():
    return {'Proyecto individual Nº1: Recomendacion de peliculas'}

@app.get('/peliculas_mes/({mes})')
def cantidad_filmaciones_mes(mes):
    # Mapea los meses en español a sus equivalentes numéricos
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }

    # Verifica si el mes ingresado es válido
    if mes.lower() not in meses:
        raise ValueError("El mes ingresado no es válido. Por favor ingrese un mes en español.")

    mes_numero = meses[mes.lower()]

    try:
        # Cargar el DataFrame desde el archivo CSV
        df_combined = pd.read_excel('./Datos_transformados.xlsx')

        # Asegúrate de que la columna 'release_date' esté en formato datetime
        df_combined['release_date'] = pd.to_datetime(df_combined['release_date'], errors='coerce')

        # Filtra las películas que fueron estrenadas en el mes especificado
        peliculas_en_mes = df_combined[df_combined['release_date'].dt.month == mes_numero]

        # Cuenta la cantidad de películas
        cantidad_peliculas = peliculas_en_mes.shape[0]

        return f"{cantidad_peliculas} películas fueron estrenadas en el mes de {mes.capitalize()}."

    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo CSV.")
        return None
    except KeyError:
        print("Error: La columna 'release_date' no está presente en el archivo CSV.")
        return None
    except ValueError as ve:
        print(f"Error al convertir la fecha: {ve}")
        return None
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return None

# Ejemplo de uso
#print(cantidad_filmaciones_mes("julio"))

#2do
@app.get('/peliculas_dia/({dia})')
def cantidad_dia_peliculas(dia: str) -> dict:
   
    # Creamos diccionario para normalizar los días en español a inglés
    days = {
        'lunes': 'Monday', 'martes': 'Tuesday','miercoles': 'Wednesday', 'jueves': 'Thursday', 'viernes': 'Friday', 'sábado': 'Saturday', 'domingo': 'Sunday'
    }

    # Convertimos el día ingresado a minúsculas y obtenemos su equivalente en inglés
    day = days.get(dia.lower(), None)

    # Verificamos si el día proporcionado es válido
    if not day:
        return {'error': f"No se encontró información para el día '{dia}'"}

    # Cargar el DataFrame desde el archivo CSV
    df_combined = pd.read_excel('./Datos_transformados.xlsx')

    # Suponiendo que 'release_date' es una columna de tipo datetime en el DataFrame df
    # Filtramos el DataFrame para obtener las películas estrenadas en el día especificado
    peliculas_dia_df = df_combined[df_combined['release_date'].dt.day_name() == day].drop_duplicates(subset='id')

    # Calculamos la cantidad de películas
    cantidad_peliculas = peliculas_dia_df.shape[0]

    # Retornamos el resultado en un diccionario
    return {'dia': dia, 'cantidad de peliculas': cantidad_peliculas}


#resultado = cantidad_dia_peliculas('miercoles')
#print(resultado)

@app.get('/titulo_filmacion/({filmacion})')
def score_titulo(titulo_de_la_filmacion: str) -> str:
     # Cargar el DataFrame desde el archivo CSV
    df_combined = pd.read_excel('./Datos_transformados.xlsx')

    # Filtramos el dataframe por el título de la filmación
    pelicula = df_combined[df_combined['title'].str.lower() == titulo_de_la_filmacion.lower()]
    
    # Si no se encuentra la película, devolvemos un mensaje indicándolo
    if pelicula.empty:
        return f"La película '{titulo_de_la_filmacion}' no fue encontrada."
    
    # Obtenemos los valores necesarios
    titulo = pelicula['title'].values[0]
    ano_estreno = pelicula['release_year'].values[0]
    score = pelicula['vote_average'].values[0]

    # Formateamos la respuesta
    respuesta = f"La película '{titulo}' fue estrenada en el año {ano_estreno} con un score/popularidad de {score}."
    
    return respuesta



#resultado = score_titulo("Jumanji")
#print(resultado)

@app.get('/titulo_de_la_filmacion/({titulo_filmacion})')
def votos_titulo(titulo_de_la_filmacion: str) -> str:

     # Cargar el DataFrame desde el archivo CSV
    df_combined = pd.read_excel('./Datos_transformados.xlsx')

    # Filtramos el dataframe por el título de la filmación
    pelicula = df_combined[df_combined['title'].str.lower() == titulo_de_la_filmacion.lower()]
    
    # Si no se encuentra la película, devolvemos un mensaje indicándolo
    if pelicula.empty:
        return f"La película '{titulo_de_la_filmacion}' no fue encontrada."
    
    # Obtenemos los valores necesarios
    titulo = pelicula['title'].values[0]
    ano_estreno = pelicula['release_year'].values[0]
    cantidad_votos = pelicula['vote_count'].values[0]
    promedio_votos = pelicula['vote_average'].values[0]
    
    # Verificamos si la película tiene al menos 2000 votos
    if cantidad_votos < 2000:
        return f"La película '{titulo}' no cuenta con al menos 2000 valoraciones."
    
    # Formateamos la respuesta
    respuesta = (f"La película '{titulo}' fue estrenada en el año {ano_estreno}. "
                 f"La misma cuenta con un total de {cantidad_votos} valoraciones, "
                 f"con un promedio de {promedio_votos}.")
    
    return respuesta


#resultado = votos_titulo("Jumanji")
#print(resultado)

@app.get('/nombre_actor/({actor})')
def get_actor(nombre_actor):
     # Cargar el DataFrame desde el archivo CSV
    df_combined = pd.read_excel('./Datos_transformados.xlsx') 
 
    # Filtrar el dataframe para obtener solo las filas donde el actor está presente
    df_actor = df_combined[df_combined['actors'].str.contains(nombre_actor, case=False, na=False)]
    
    # Calcular la cantidad de películas
    cantidad_peliculas = df_actor.shape[0]
    
    # Calcular el total de retorno
    total_retorno = df_actor['return'].sum()
    
    # Calcular el promedio de retorno
    promedio_retorno = df_actor['return'].mean()
    
    # Formatear el mensaje de salida
    mensaje = (f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, "
               f"el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación.")
    
    return mensaje

#Ejemplo de uso:
#print(get_actor("Robin Williams"))

@app.get('/nombre_director/({director})')
def get_director(nombre_director):
     # Cargar el DataFrame desde el archivo CSV
    df_combined = pd.read_excel('./Datos_transformados.xlsx') 

    # Filtrar el DataFrame para obtener solo las filas del director dado
    director_data = df_combined[df_combined['director'] == nombre_director]
    
    # Verificar si se encontraron películas del director
    if director_data.empty:
        return f"No se encontraron películas del director {nombre_director}"
    
    # Calcular el retorno total del director
    total_return = director_data['return'].sum()
    
    # Crear una lista para almacenar la información de cada película
    movies_info = []
    
    for index, row in director_data.iterrows():
        movie_info = {
            'title': row['title'],
            'release_date': row['release_date'],
            'revenue': row['revenue'],
        }
        movies_info.append(movie_info)
    
    # Crear el resultado final
    result = {
        'director': nombre_director,
        'total_return': total_return,
        'movies': movies_info
    }
    
    return result
#nombre_director = 'John Lasseter'
#print(get_director(nombre_director))