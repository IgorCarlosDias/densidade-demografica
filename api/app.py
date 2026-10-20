import os
import re
from collections import Counter
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configura templates e static
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app = FastAPI(title="Densidade Demográfica - iNaturalist")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

INAT_API = "https://api.inaturalist.org/v1"
TIMEOUT = 10

# Categorias da Lista Vermelha da IUCN (código numérico usado pelo iNaturalist)
IUCN = {
    10: ("LC", "Pouco preocupante"),
    20: ("NT", "Quase ameaçada"),
    30: ("VU", "Vulnerável"),
    40: ("EN", "Em perigo"),
    50: ("CR", "Criticamente em perigo"),
    60: ("EW", "Extinta na natureza"),
    70: ("EX", "Extinta"),
}

RANKS_PT = {
    "kingdom": "Reino", "phylum": "Filo", "class": "Classe", "order": "Ordem",
    "family": "Família", "genus": "Gênero", "species": "Espécie",
}


def _strip_html(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def _parse_location(obs: dict):
    location = obs.get("location")
    if isinstance(location, str) and "," in location:
        try:
            lat, lon = map(float, location.split(","))
            return lat, lon
        except ValueError:
            return None, None
    if isinstance(location, dict):
        return location.get("latitude"), location.get("longitude")
    return None, None


def _obs_photo(obs: dict) -> Optional[str]:
    photos = obs.get("photos") or []
    if photos and photos[0].get("url"):
        return photos[0]["url"].replace("square", "medium")
    return None


def buscar_taxon(taxon_id: int) -> Optional[dict]:
    """Busca detalhes educativos do táxon (resumo, conservação, taxonomia)."""
    try:
        r = requests.get(f"{INAT_API}/taxa/{taxon_id}", params={"locale": "pt"}, timeout=TIMEOUT)
        if r.status_code != 200 or not r.json().get("results"):
            return None
        t = r.json()["results"][0]
    except (requests.RequestException, ValueError):
        return None

    conservacao = None
    cs = t.get("conservation_status")
    if cs and cs.get("iucn") in IUCN:
        code, label = IUCN[cs["iucn"]]
        conservacao = {"code": code, "label": label, "authority": cs.get("authority") or "IUCN"}

    taxonomia = [
        {"rank": RANKS_PT[a["rank"]], "name": a.get("name")}
        for a in t.get("ancestors", [])
        if a.get("rank") in RANKS_PT
    ]
    if t.get("rank") in RANKS_PT:
        taxonomia.append({"rank": RANKS_PT[t["rank"]], "name": t.get("name")})

    photo = (t.get("default_photo") or {}).get("medium_url")
    return {
        "id": t.get("id"),
        "name": t.get("name"),
        "common_name": t.get("preferred_common_name") or t.get("name"),
        "photo": photo,
        "attribution": (t.get("default_photo") or {}).get("attribution", ""),
        "summary": _strip_html(t.get("wikipedia_summary")),
        "wikipedia_url": t.get("wikipedia_url"),
        "observations_count": t.get("observations_count", 0),
        "iconic": t.get("iconic_taxon_name"),
        "conservacao": conservacao,
        "taxonomia": taxonomia,
    }


def buscar_observacoes(especie: str) -> dict:
    observacoes = []
    params = {"q": especie, "per_page": 200, "locale": "pt", "photos": "true"}
    try:
        response = requests.get(f"{INAT_API}/observations", params=params, timeout=TIMEOUT)
        results = response.json().get("results", []) if response.status_code == 200 else []
    except (requests.RequestException, ValueError) as e:
        print(f"Erro ao consultar iNaturalist API: {e}")
        results = []

    taxon_counter = Counter()
    for obs in results:
        lat, lon = _parse_location(obs)
        if lat is None or lon is None:
            continue
        taxon = obs.get("taxon") or {}
        if taxon.get("id"):
            taxon_counter[taxon["id"]] += 1
        observacoes.append({
            "id": obs.get("id"),
            "preferred_common_name": taxon.get("preferred_common_name") or taxon.get("name") or "Nome não encontrado",
            "scientific_name": taxon.get("name") or "",
            "iconic": taxon.get("iconic_taxon_name") or "Unknown",
            "place_guess": obs.get("place_guess") or "Localização desconhecida",
            "observed_on": obs.get("observed_on"),
            "quality": obs.get("quality_grade"),
            "observer": (obs.get("user") or {}).get("login"),
            "lat": lat,
            "lon": lon,
            "photo": _obs_photo(obs) or (taxon.get("default_photo") or {}).get("medium_url"),
            "wikipedia_url": taxon.get("wikipedia_url"),
        })

    taxon_info = None
    if taxon_counter:
        taxon_info = buscar_taxon(taxon_counter.most_common(1)[0][0])

    anos = sorted(int(o["observed_on"][:4]) for o in observacoes if o.get("observed_on"))
    stats = {
        "total": len(observacoes),
        "pesquisa": sum(1 for o in observacoes if o["quality"] == "research"),
        "observadores": len({o["observer"] for o in observacoes if o["observer"]}),
        "periodo": f"{anos[0]}–{anos[-1]}" if anos and anos[0] != anos[-1] else (str(anos[0]) if anos else "—"),
    }
    return {"observacoes": observacoes, "taxon": taxon_info, "stats": stats}


def render(request: Request, especie: Optional[str]):
    especie = (especie or "").strip()
    data = buscar_observacoes(especie) if especie else {"observacoes": [], "taxon": None, "stats": None}
    return templates.TemplateResponse(
        "mapa.html",
        {"request": request, "especie": especie, **data},
    )


@app.get("/", response_class=HTMLResponse)
def index_get(request: Request, especie: Optional[str] = None):
    return render(request, especie)


@app.post("/", response_class=HTMLResponse)
def index_post(request: Request, especie: str = Form(None)):
    return render(request, especie)
