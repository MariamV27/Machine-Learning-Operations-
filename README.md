                              
                                         Proyecto de Transformaciones de Datos y API de Películas


![enter image description here](https://blog.soyhenry.com/content/images/2022/12/Data_logo.png)
Este repositorio contiene un proyecto orientado a la transformación de datos de películas y la creación de una API utilizando FastAPI para consultar información relevante sobre las mismas.

## Transformaciones de Datos

En este MVP, se realizaron las siguientes transformaciones sobre los datos:

- **Desanidación de Campos**: Se desanidaron campos como `belongs_to_collection`, `production_companies`,`cast`,	`crew`,	`id`.
- **Limpieza de Datos Nulos**: Se rellenaron los valores nulos en `revenue` y `budget` con cero, y se eliminaron los nulos en `release_date`.
- **Formato de Fechas**: Se aseguró que las fechas tuvieran el formato AAAA-mm-dd y se creó la columna `release_year` para almacenar el año de estreno.
- **Cálculo de Retorno de Inversión**: Se creó la columna `return` calculando el retorno de inversión como `revenue / budget`, considerando cero cuando no hay datos disponibles.
- **Eliminación de Columnas**: Se eliminaron las columnas que no serán utilizadas en el proyecto: `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage`.

## Desarrollo de API con FastAPI

Se desarrolló una API utilizando FastAPI para proporcionar acceso a los datos de películas anteriormente extraidos. Se implementaron los siguientes endpoints:

1. **cantidad_filmaciones_mes(Mes)**: Retorna la cantidad de películas estrenadas en un mes específico.
2. **cantidad_filmaciones_dia(Dia)**: Retorna la cantidad de películas estrenadas en un día específico.
3. **score_titulo(titulo_de_la_filmación)**: Retorna el título, año de estreno y score/popularidad de una película dado su título.
4. **votos_titulo(titulo_de_la_filmación)**: Retorna el título, cantidad de votos y promedio de votaciones de una película, con un mínimo de 2000 valoraciones.
5. **get_actor(nombre_actor)**: Retorna la cantidad de filmaciones, retorno total y promedio por filmación de un actor.
6. **get_director(nombre_director)**: Retorna el éxito de un director, incluyendo nombres de películas, fechas de lanzamiento, retorno, costo y ganancia.

## Deployment

El servicio se puede desplegar utilizando servicios como Render, Railway u otros que permitan la exposición de una API web.

## Análisis Exploratorio de Datos (EDA)

Se realizó un análisis exploratorio de datos para identificar relaciones entre variables, detectar outliers y buscar patrones interesantes. Se utilizaron herramientas como pandas matplotlib.pyplot, pandas, autoviz,nltk,wordcloud, entre otros.

## Sistema de Recomendación

Se implementó un sistema de recomendación de películas basado en la similitud de puntajes. El sistema retorna una lista de 5 películas similares dado el nombre de una película de entrada.
