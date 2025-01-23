# Importa as bibliotecas necessárias
from flask import Flask, render_template, request  # Flask para criar a aplicação web, render_template para renderizar HTML e request para capturar dados da requisição
import requests  # Usado para realizar requisições HTTP
from waitress import serve  # Usado para iniciar o servidor

# Instancia a aplicação Flask
app = Flask(__name__)

# Define a rota principal e os métodos HTTP permitidos (GET e POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    especie = None  # Inicializa a variável para armazenar o nome da espécie pesquisada
    observacoes = []  # Lista para armazenar as observações retornadas pela API

    # Verifica se a requisição foi enviada via método POST
    if request.method == 'POST':
        especie = request.form.get('especie')  # Obtém o valor do campo 'especie' enviado pelo formulário
        if especie:  # Verifica se o usuário digitou alguma espécie
            url = 'https://api.inaturalist.org/v1/observations'  # URL base da API do iNaturalist
            params = {
                'q': especie,  # Especifica a espécie a ser pesquisada
                'per_page': 200,  # Limita o retorno a 200 resultados por página
                'locale': 'pt',  # Tenta retornar os nomes comuns no idioma português
            }
            response = requests.get(url, params=params)  # Faz a requisição GET para a API com os parâmetros

            # Verifica se a requisição foi bem-sucedida (código HTTP 200)
            if response.status_code == 200:
                data = response.json()  # Converte o conteúdo da resposta para um dicionário Python

                # Verifica se os dados retornados contêm uma chave 'results'
                if isinstance(data, dict) and 'results' in data:
                    resultados = data['results']  # Armazena a lista de observações na variável 'resultados'

                    # Itera sobre cada observação retornada pela API
                    for obs in resultados:
                        if isinstance(obs, dict):  # Garante que a observação seja um dicionário
                            location = obs.get('location')  # Obtém a localização da observação (latitude e longitude)
                            preferred_common_name = obs.get('taxon', {}).get('preferred_common_name', 'Nome não encontrado')  # Nome comum
                            scientific_name = obs.get('taxon', {}).get('name', 'Nome científico não encontrado')  # Nome científico
                            observation_id = obs.get('id')  # ID único da observação
                            user_name = obs.get('user', {}).get('name', 'Usuário não encontrado')  # Nome do usuário que registrou a observação
                            created_at = obs.get('created_at')  # Data e hora da criação da observação
                            description = obs.get('description', 'Descrição não fornecida')  # Descrição da observação
                            place_guess = obs.get('place_guess', 'Localização desconhecida')  # Nome aproximado do local
                            wikipedia_url = obs.get('taxon', {}).get('wikipedia_url', 'Link não cadastrado')  # Link da Wikipedia

                            # Tenta acessar a foto da observação, se disponível
                            default_photo = obs.get('taxon', {}).get('default_photo', None)
                            if default_photo and isinstance(default_photo, dict):
                                medium_url = default_photo.get('medium_url', 'Imagem não encontrada')
                            else:
                                medium_url = 'Imagem não encontrada'

                            # Inicializa latitude e longitude como None por padrão
                            lat, lon = None, None

                            # Processa a localização (latitude e longitude) da observação
                            if isinstance(location, str):
                                if ',' in location:
                                    lat, lon = location.split(',')
                                    lat = float(lat) if lat else None
                                    lon = float(lon) if lon else None
                            elif isinstance(location, dict):  # Caso a localização seja um dicionário
                                lat = location.get('latitude')
                                lon = location.get('longitude')

                            # Garante que a observação só seja adicionada se a localização for válida
                            if lat is not None and lon is not None:
                                observacoes.append({
                                    'id': observation_id,
                                    'preferred_common_name': preferred_common_name,
                                    'scientific_name': scientific_name,
                                    'user_name': user_name,
                                    'created_at': created_at,
                                    'description': description,
                                    'place_guess': place_guess,
                                    'lat': lat,  # Latitude
                                    'lon': lon,  # Longitude
                                    'medium_url': medium_url,  # URL da foto
                                    'wikipedia_url': wikipedia_url  # Link para a Wikipedia
                                })
                else:
                    print("Nenhuma observação encontrada para a espécie.")  # Caso não haja resultados
            else:
                print(f"Erro na requisição: {response.status_code}")  # Mensagem de erro caso a requisição falhe

    # Renderiza o template HTML 'mapa.html', passando os dados da espécie e observações
    return render_template('mapa.html', especie=especie, observacoes=observacoes)

# Executa a aplicação em produção
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
