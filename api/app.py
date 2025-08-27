import os
from flask import Flask, request, jsonify, render_template
import requests
from mangum import Mangum

# Corrige os caminhos de templates e static para serverless / subpasta api
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

@app.route("/", methods=["GET", "POST"])
def index():
    especie = request.form.get("especie") if request.method == "POST" else request.args.get("especie")
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

    return render_template("mapa.html", observacoes=observacoes, especie=especie)

# Handler necessário para Vercel serverless
handler = Mangum(app)
