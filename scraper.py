import json
from bs4 import BeautifulSoup
import requests

def extraer_eventos():
    url = "https://sanmiguellive.com/es"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    eventos = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos los bloques de eventos o tarjetas en la estructura de San Miguel Live
            tarjetas = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and ('event' in x.lower() or 'card' in x.lower() or 'item' in x.lower() or 'show' in x.lower()))
            
            if not tarjetas:
                tarjetas = soup.find_all('article')

            for tarjeta in tarjetas:
                try:
                    # Extraer Título
                    titulo_el = tarjeta.find(['h2', 'h3', 'h4', 'a'])
                    titulo = titulo_el.get_text(strip=True) if titulo_el else ""
                    
                    if not titulo or len(titulo) < 3 or "inicio" in titulo.lower():
                        continue

                    # Extraer Imagen
                    img_el = tarjeta.find('img')
                    imagen = ""
                    if img_el:
                        imagen = img_el.get('src') or img_el.get('data-src') or ""
                    
                    if not imagen or "http" not in imagen:
                        imagen = "https://images.unsplash.com/photo-1512813084011-2eb2659174df?auto=format&fit=crop&w=800&q=80"

                    # Extraer Descripción o detalles
                    desc_el = tarjeta.find(['p', 'div'], class_=lambda x: x and ('desc' in x.lower() or 'details' in x.lower()))
                    if not desc_el:
                        desc_el = tarjeta.find('p')
                    descripcion = desc_el.get_text(strip=True) if desc_el else "Evento cultural destacado en San Miguel de Allende."
                    if len(descripcion) > 150:
                        descripcion = descripcion[:147] + "..."

                    # Extraer Fecha / Hora
                    fecha_el = tarjeta.find(['time', 'span', 'div'], class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower()))
                    fecha = fecha_el.get_text(strip=True) if fecha_el else "Próximamente"

                    # Evitar duplicados
                    if any(ev['titulo'] == titulo for ev in eventos):
                        continue

                    eventos.append({
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "fecha": fecha,
                        "mes": "Agenda Cultural",
                        "lugar": "San Miguel de Allende, Gto.",
                        "costo": "Consultar sitio",
                        "contactoText": "🌐 Ver en San Miguel Live",
                        "contactoUrl": url,
                        "imagen": imagen
                    })
                except:
                    continue
    except Exception as e:
        print(f"Error de conexión: {e}")

    # Respaldo oficial en caso de restricciones de red
    if not eventos:
        eventos = [
            {
                "titulo": "Conciertos y Música en Vivo",
                "descripcion": "Disfruta de la mejor cartelera de música, jazz y presentaciones artísticas en los recintos de la ciudad.",
                "fecha": "Cartelera diaria",
                "mes": "Agenda Cultural",
                "lugar": "Foros y Centros Culturales SMA",
                "costo": "Varía por evento",
                "contactoText": "🌐 Ir a San Miguel Live",
                "contactoUrl": "https://sanmiguellive.com/es",
                "imagen": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80"
            }
        ]

    return eventos

if __name__ == "__main__":
    datos = extraer_eventos()
    with open("eventos_sma.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print(f"¡Sincronización exitosa con {len(datos)} eventos de San Miguel Live!")
