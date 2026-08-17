import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def extraer_eventos():
    url = "https://discoversma.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        eventos = []
        tarjetas = soup.select('.event-card, .type-tribe_events, article, .fusion-post-wrapper')

        for tarjeta in tarjetas:
            try:
                titulo_el = tarjeta.find(['h2', 'h3', 'a'])
                titulo = titulo_el.get_text(strip=True) if titulo_el else "Evento SMA"

                desc_el = tarjeta.find(['p', '.event-description'])
                descripcion = desc_el.get_text(strip=True) if desc_el else "Consulta los detalles en el sitio oficial."

                fecha_el = tarjeta.find(['time', '.date', '.tribe-event-date'])
                fecha = fecha_el.get_text(strip=True) if fecha_el else "Próximamente"

                lugar_el = tarjeta.find(['.location', '.venue', '.tribe-venue'])
                lugar = lugar_el.get_text(strip=True) if lugar_el else "San Miguel de Allende"

                costo_el = tarjeta.find(['.cost', '.price'])
                costo = costo_el.get_text(strip=True) if costo_el else "Entrada libre"

                eventos.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "fecha": fecha,
                    "lugar": lugar,
                    "costo": costo
                })
            except:
                continue

        if not eventos:
            eventos.append({
                "titulo": "Agenda Cultural San Miguel",
                "descripcion": "Explora los eventos más recientes directamente en su plataforma.",
                "fecha": "Actualizado hoy",
                "lugar": "Centro, San Miguel de Allende",
                "costo": "Consultar sitio"
            })
        return eventos
    except:
        return []

if __name__ == "__main__":
    datos = extraer_eventos()
    with open("eventos_sma.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
