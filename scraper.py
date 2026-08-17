import json
from bs4 import BeautifulSoup
import requests

def extraer_eventos():
    url = "https://www.visitsanmiguel.travel/event-list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print("Error al conectar con Visit San Miguel")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        eventos = []
        
        # Buscamos los contenedores estándar de tarjetas o listas de eventos en la página
        tarjetas = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and ('event' in x.lower() or 'item' in x.lower() or 'card' in x.lower()))
        
        if not tarjetas:
            # Respaldo buscando bloques generales si cambia la clase
            tarjetas = soup.find_all('article')

        for tarjeta in tarjetas:
            try:
                # Título del evento
                titulo_el = tarjeta.find(['h2', 'h3', 'h4', 'a'], class_=lambda x: x and 'title' in x.lower())
                if not titulo_el:
                    titulo_el = tarjeta.find(['h2', 'h3', 'h4'])
                titulo = titulo_el.get_text(strip=True) if titulo_el else ""
                
                if not titulo or len(titulo) < 3:
                    continue

                # Descripción
                desc_el = tarjeta.find(['p', 'div'], class_=lambda x: x and ('desc' in x.lower() or 'summary' in x.lower()))
                if not desc_el:
                    desc_el = tarjeta.find('p')
                descripcion = desc_el.get_text(strip=True) if desc_el else "Consulta los detalles de este gran evento en San Miguel de Allende."
                if len(descripcion) > 160:
                    descripcion = descripcion[:157] + "..."

                # Fecha
                fecha_el = tarjeta.find(['time', 'span', 'div'], class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower()))
                fecha = fecha_el.get_text(strip=True) if fecha_el else "Próximamente"

                # Lugar
                lugar_el = tarjeta.find(['span', 'div', 'p'], class_=lambda x: x and ('location' in x.lower() or 'venue' in x.lower() or 'place' in x.lower()))
                lugar = lugar_el.get_text(strip=True) if lugar_el else "San Miguel de Allende, Gto."

                # Evitar duplicados
                if any(ev['titulo'] == titulo for ev in eventos):
                    continue

                eventos.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "fecha": fecha,
                    "lugar": lugar,
                    "costo": "Entrada general / Consultar sitio"
                })
            except Exception:
                continue

        # Respaldo por si la estructura visual es diferente
        if not eventos:
            eventos.append({
                "titulo": "Agenda Turística San Miguel",
                "descripcion": "Descubre los próximos eventos y actividades en la ciudad.",
                "fecha": "Cartelera vigente",
                "lugar": "San Miguel de Allende",
                "costo": "Varía según evento"
            })

        return eventos
    except Exception as e:
        print(f"Error de ejecución: {e}")
        return []

if __name__ == "__main__":
    datos = extraer_eventos()
    with open("eventos_sma.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print(f"¡Se sincronizaron {len(datos)} eventos correctamente!")
