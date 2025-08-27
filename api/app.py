import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from fastapi.staticfiles import StaticFiles

# Define diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cria app
app = FastAPI()

# Configura templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Monta static
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def index(request: Request, especie: str = Form(None)):
    observacoes = []

    if especie:
        url = "https://api.inaturalist.org/v1/observations"
        params = {"q": especie, "per_page": 200, "locale": "pt"}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for obs in data.get("results", []):
                location = obs.get("location")
                preferred_common_name = obs.get("taxon", {}).get("preferred_common_name", "Nome não encontrado")
                scientific_name = obs.get("taxon", {}).get("name", "Nome científico não encontrado")
                observation_id = obs.get("id")
                place_guess = obs.get("place_guess", "Localização desconhecida")
                wikipedia_url = obs.get("taxon", {}).get("wikipedia_url", "Link não cadastrado")
                medium_url = obs.get("taxon", {}).get("default_photo", {}).get("medium_url", "Imagem não encontrada")

                lat, lon = None, None
                if isinstance(location, str) and "," in location:
                    lat, lon = map(float, location.split(","))
                elif isinstance(location, dict):
                    lat = location.get("latitude")
                    lon = location.get("longitude")

                if lat is not None and lon is not None:
                    observacoes.append({
                        "id": observation_id,
                        "preferred_common_name": preferred_common_name,
                        "scientific_name": scientific_name,
                        "place_guess": place_guess,
                        "lat": lat,
                        "lon": lon,
                        "medium_url": medium_url,
                        "wikipedia_url": wikipedia_url
                    })

    return templates.TemplateResponse("mapa.html", {"request": request, "observacoes": observacoes, "especie": especie})
