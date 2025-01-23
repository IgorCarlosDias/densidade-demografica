Densidade Demográfica - iNaturalist
Este projeto utiliza a API do iNaturalist para buscar observações de espécies e exibir essas informações em um mapa interativo. O objetivo é permitir a pesquisa por espécies, visualizar suas observações e mostrar detalhes, como localização, foto e link para a Wikipedia.

Funcionalidades
Pesquisa de espécies através da API do iNaturalist.
Exibição de observações com informações detalhadas: nome comum e científico, localização (latitude e longitude), foto (se disponível), descrição e link para Wikipedia.
Exibição das observações em um mapa interativo.
Tecnologias Utilizadas
Flask: Framework Python para o desenvolvimento da aplicação web.
Waitress: Servidor WSGI para rodar a aplicação em produção.
iNaturalist API: API externa para buscar observações de espécies.
HTML/CSS/JavaScript: Para o front-end e exibição do mapa.
Instalação
1. Clonar o Repositório
Clone este repositório para a sua máquina:

bash
Copiar
Editar
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
csharp
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
Crie uma branch para a sua feature (git checkout -b feature/nova-feature).
Comite suas mudanças (git commit -am 'Adicionando nova feature').
Push na branch (git push origin feature/nova-feature).
Abra um Pull Request.
Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.