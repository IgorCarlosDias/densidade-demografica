# Densidade Demográfica - iNaturalist

Este projeto utiliza a API do iNaturalist para buscar observações de espécies ao redor do mundo e exibir essas informações em um mapa interativo com Leaflet.js. O objetivo é permitir a pesquisa por espécies (nome popular ou científico), visualizar suas observações e mostrar detalhes como localização, foto e link para a Wikipedia.

---

## Funcionalidades

- **Pesquisa de espécies** através da API pública do iNaturalist.
- **Exibição de observações** com informações detalhadas:
  - Nome comum e científico
  - Localização aproximada (latitude e longitude)
  - Foto do espécime (quando disponível)
  - Link direto para a observação e verbete na Wikipedia
- **Mapa interativo (Leaflet.js)** com enquadramento automático de zoom nos pontos encontrados.
- Pronto para execução local e deploy na Vercel (Serverless Python).

---

## Tecnologias Utilizadas

- **FastAPI**: Framework Python moderno e assíncrono para o backend.
- **Uvicorn**: Servidor ASGI de alta performance para execução local.
- **Jinja2**: Motor de templates HTML.
- **Leaflet.js & OpenStreetMap**: Para renderização de mapas interativos.
- **iNaturalist API**: API externa para consulta de dados de biodiversidade.

---

## Estrutura do Projeto

```text
densidade-demografica/
├── api/
│   ├── app.py              # Aplicação principal FastAPI
│   ├── static/
│   │   └── css/
│   │       └── styles.css  # Folha de estilo
│   └── templates/
│       └── mapa.html       # Template com mapa Leaflet e interface de busca
├── run.py                  # Script para inicialização local
├── requirements.txt        # Dependências do projeto
├── vercel.json             # Configuração para deploy serverless na Vercel
└── README.md
```

---

## Instalação e Execução Local

### 1. Clonar o Repositório

```bash
git clone https://github.com/IgorCarlosDias/densidade-demografica.git
cd densidade-demografica
```

### 2. Criar e Ativar o Ambiente Virtual

No Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a Aplicação

Você pode rodar diretamente com o script `run.py`:
```bash
python run.py
```

Ou usando o Uvicorn com hot-reload:
```bash
uvicorn api.app:app --reload --port 8080
```

Abra seu navegador em [http://localhost:8080](http://localhost:8080).
