# API de Detecção de Idioma e Análise de Sentimentos

Este projeto implementa uma API RESTful para detecção de idioma e análise de sentimentos, construída com FastAPI.

## Contexto Acadêmico

Este sistema foi desenvolvido como parte da disciplina "Construção de APIs para Inteligência Artificial" do programa de Pós-Graduação em Sistemas e Agentes Inteligentes da Universidade Federal de Goiás (UFG).

- **Disciplina:** Construção de APIs para Inteligência Artificial
- **Pós-Graduação:** Sistemas e Agentes Inteligentes ([https://agentes.inf.ufg.br/](https://agentes.inf.ufg.br/))
- **Universidade:** Universidade Federal de Goiás ([https://ufg.br/](https://ufg.br/))
- **Alunos:** Célio Carcalto e Anahi Philbois

## Visão Geral

A API oferece dois endpoints principais:

1.  **Detecção de Idioma:** Identifica o idioma de um texto fornecido.
2.  **Análise de Sentimentos:** Analisa o sentimento de um texto (positivo, negativo ou neutro) e fornece scores de polaridade e subjetividade.

Para uma documentação detalhada da API, incluindo arquitetura, configuração, endpoints e mecanismos de IA, consulte o arquivo [DOCUMENTATION.md](DOCUMENTATION.md).

## Como Executar

1.  **Clone o repositório:**

    ```bash
    git clone <URL_do_repositório>  # Substitua pela URL do repositório
    cd TrabalhoPOSufgAPI
    ```
2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```
4. **Configure a API Key:**
    Configure a variável de ambiente `API_KEY` no arquivo `.env` ou diretamente no ambiente do sistema.

5.  **Execute a API:**

    ```bash
    uvicorn app.main:app --reload
    ```

A documentação interativa da API estará disponível em:

-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE) (Nota: É preciso criar um arquivo LICENSE, se for o caso).
