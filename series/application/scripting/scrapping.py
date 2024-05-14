import re
import requests
from bs4 import BeautifulSoup
import urllib
import time


def find_links(url):
    req = requests.get(url)

    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        html = BeautifulSoup(req.text, "html.parser")

        # Obtenemos todos los enlaces
        enlaces = html.find_all('a')

        # Recorremos todos los enlaces para extraer aquellos que contienen las extensiones deseadas
        parent_directory_url = None
        subtitulo = None
        portada = None
        for i, enlace in enumerate(enlaces):
            href = enlace.get('href')
            text = enlace.string
            if text == 'Parent Directory':
                parent_directory_url = urllib.parse.urljoin(url, href)
            elif text not in ['Name', 'Last modified', 'Size', 'Description', 'ayuda']:
                if href and (href.endswith('.mkv') or href.endswith('.mp4') or href.endswith('.mpg') or href.endswith('.avi') or href.endswith('.AVI')
                             or href.endswith('.MPG') or href.endswith('.MP4') or href.endswith('.MKV') or href.endswith('.srt') or href.endswith('.jpg')):
                    
                    # Extraer el nombre de la serie del directorio actual
                    nombre_serie = url.split('/')[-3]
                    temporada = url.split('/')[-2]

                    capitulo = href.split('%20')[0]
                    capitulo = capitulo.split('x')[1]

                    # Guardar las URLs de los archivos .srt y .jpg
                    if href.endswith('.srt'):
                        subtitulo = url + href
                    elif href.endswith('.jpg'):
                        portada = url + href

                    print(f"Serie: {nombre_serie}")
                    print(f"Temporada: {temporada}")
                    print(f"Capitulo: {capitulo}")
                    print("Video: {}".format(url+href))
                    if subtitulo:
                        print("Subtítulo: {}".format(subtitulo))
                    if portada:
                        print("Portada: {}".format(portada))

                elif href:
                    new_url = urllib.parse.urljoin(url, href)
                    time.sleep(3)
                    find_links(new_url)

    else:
        print("Status Code %d" % statusCode)

# URL de la página web
url = "https://visuales.uclv.cu/Series/Espanol/Aida/S05/"

# Iniciamos la búsqueda
find_links(url)

