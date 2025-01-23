# Densidade Demográfica - iNaturalist

Este projeto utiliza a API do iNaturalist para buscar observações de espécies e exibir essas informações em um mapa interativo. O objetivo é permitir a pesquisa por espécies, visualizar suas observações e mostrar detalhes, como localização, foto e link para a Wikipedia.

---

## Funcionalidades

- **Pesquisa de espécies** através da API do iNaturalist.  
- **Exibição de observações** com informações detalhadas:  
  - Nome comum e científico  
  - Localização (latitude e longitude)  
  - Foto (se disponível)  
  - Descrição e link para Wikipedia  
- **Mapa interativo** para visualização das observações.

---

## Tecnologias Utilizadas

- **Flask**: Framework Python para o desenvolvimento da aplicação web.  
- **Waitress**: Servidor WSGI para rodar a aplicação em produção.  
- **iNaturalist API**: API externa para buscar observações de espécies.  
- **HTML/CSS/JavaScript**: Para o front-end e exibição do mapa.

---

## Instalação

### 1. Clonar o Repositório

Clone este repositório para a sua máquina:

```bash
git clone https://github.com/seu-usuario/densidade-demografica.git
cd densidade-demografica
2. Criar e Ativar o Ambiente Virtual
Crie e ative o ambiente virtual para o projeto:

No Windows:

bash
Copiar
Editar
python -m venv venv
.\venv\Scripts\activate
No macOS/Linux:

bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate
3. Instalar as Dependências
Instale as dependências necessárias usando pip:

bash
Copiar
Editar
pip install -r requirements.txt
4. Rodar a Aplicação
Para rodar a aplicação, execute o seguinte comando:

bash
Copiar
Editar
python app.py
O servidor será iniciado na porta 8080. Você pode acessar a aplicação no navegador através de:

arduino
Copiar
Editar
http://localhost:8080
Estrutura do Projeto
plaintext
Copiar
Editar
.
├── app.py                # Arquivo principal da aplicação Flask
├── requirements.txt      # Dependências do projeto
├── templates/            # Contém os templates HTML
│   └── mapa.html         # Template para exibição do mapa e observações
└── static/               # Arquivos estáticos (CSS, JS, Imagens)
    └── styles.css        # Estilo do front-end
Contribuições
Fork o projeto.
Crie uma branch para a sua feature:
bash
Copiar
Editar
git checkout -b feature/nova-feature
Comite suas mudanças:
bash
Copiar
Editar
git commit -am 'Adicionando nova feature'
Push na branch:
bash
Copiar
Editar
git push origin feature/nova-feature
Abra um Pull Request.
