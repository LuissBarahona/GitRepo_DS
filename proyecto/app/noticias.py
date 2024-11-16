import requests
from datetime import datetime

NEWS_API_KEY = '99fde377df2f4d1082857bb8042dedfe'

def obtener_noticias():
    url = ('https://newsapi.org/v2/everything?q=embedded%20systems%20OR%20electronics&'
           'sortBy=publishedAt&apiKey=' + NEWS_API_KEY)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        noticias = response.json().get('articles', [])
        
        for noticia in noticias:
            if 'publishedAt' in noticia:
                noticia['publishedAt'] = datetime.strptime(
                    noticia['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
                ).strftime('%d/%m/%Y')

        return noticias[:8]
        
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener noticias: {e}")
        return []
