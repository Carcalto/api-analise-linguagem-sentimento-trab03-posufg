# Documentação da API de IA

## Visão Geral

Este projeto consiste em uma API RESTful construída com FastAPI, projetada para fornecer serviços de inteligência artificial, especificamente detecção de idioma e análise de sentimentos em textos. A API é protegida por autenticação via API Key e possui rate limiting para garantir a estabilidade e segurança.

## Funcionalidades

1.  **Detecção de Idioma**: Permite identificar o idioma de um texto fornecido pelo usuário.
    -   **Mecanismo de Detecção de Idioma**: A detecção de idioma é realizada utilizando a biblioteca `langdetect`. Esta biblioteca utiliza uma abordagem estatística para identificar o idioma de um texto, analisando padrões de caracteres e palavras. É eficaz para identificar idiomas em textos de tamanho considerável, mas pode ter limitações com textos muito curtos ou ambíguos.

2.  **Análise de Sentimentos**: Analisa o sentimento de um texto, classificando-o como positivo, negativo ou neutro, além de fornecer scores de polaridade e subjetividade.
    -   **Mecanismo de Análise de Sentimentos**: A análise de sentimentos é implementada com a biblioteca `TextBlob`. TextBlob utiliza uma abordagem baseada em léxico, onde cada palavra no texto é avaliada com base em um dicionário de sentimentos. A polaridade do sentimento varia de -1 (negativo) a 1 (positivo), e a subjetividade de 0 (objetivo) a 1 (subjetivo). A classificação geral do sentimento (positivo, negativo, neutro) é derivada da polaridade. **Atualmente, a análise de sentimentos suporta apenas o idioma inglês.**

## Mecanismos de IA Detalhados

### Detecção de Idioma

A API utiliza a biblioteca `langdetect` para realizar a detecção de idioma. O processo funciona da seguinte maneira:

1.  **Análise Estatística**: `langdetect` analisa o texto fornecido utilizando modelos estatísticos probabilísticos. Esses modelos são treinados em grandes corpora de texto em vários idiomas.
2.  **Identificação de Padrões**: A biblioteca identifica padrões de n-gramas (sequências de caracteres) e a frequência de palavras que são característicos de cada idioma.
3.  **Determinação do Idioma Mais Provável**: Com base na análise estatística, `langdetect` determina o idioma mais provável do texto e retorna o código ISO 639-1 correspondente (e.g., "en" para inglês, "pt" para português).

É importante notar que a precisão da detecção de idioma pode variar dependendo do tamanho e da clareza do texto. Textos muito curtos ou que misturam idiomas podem ser menos precisos na detecção.

### Análise de Sentimentos

Para a análise de sentimentos, a API emprega a biblioteca `TextBlob`. O mecanismo de análise de sentimentos é baseado em léxico:

1.  **Léxico de Sentimentos**: `TextBlob` possui um léxico interno, que é um dicionário de palavras onde cada palavra é associada a scores de polaridade e subjetividade.
2.  **Tokenização e Análise Lexical**: O texto de entrada é tokenizado em palavras, e cada palavra é procurada no léxico de sentimentos.
3.  **Cálculo da Polaridade e Subjetividade**:
    -   **Polaridade**: Para cada palavra no texto que está presente no léxico, a polaridade é agregada. A polaridade final do texto é um valor que varia de -1.0 a 1.0, onde:
        -   Valores próximos de 1.0 indicam um sentimento positivo.
        -   Valores próximos de -1.0 indicam um sentimento negativo.
        -   Valores próximos de 0.0 indicam um sentimento neutro.
    -   **Subjetividade**: A subjetividade determina o quão opinativo é o texto, variando de 0.0 a 1.0, onde:
        -   Valores próximos de 0.0 indicam texto objetivo.
        -   Valores próximos de 1.0 indicam texto subjetivo.
4.  **Classificação do Sentimento**: Com base no valor da polaridade, o sentimento é classificado em:
    -   Positivo: polaridade > 0.2
    -   Negativo: polaridade < -0.2
    -   Neutro: polaridade entre -0.2 e 0.2

Este método é eficaz para muitas aplicações, mas pode ter limitações em contextos mais complexos, como sarcasmo ou ironia, onde a análise baseada em léxico pode não capturar as nuances do sentimento. **Além disso, o modelo atual suporta apenas o idioma inglês.**

## Arquitetura

O projeto está estruturado em módulos para melhor organização e escalabilidade:

-   `app/`: Contém o código principal da aplicação.
    -   `api/`: Define as rotas da API.
        -   `v1/`: Versão 1 da API.
            -   `endpoints.py`: Define os endpoints para detecção de idioma e análise de sentimentos.
    -   `core/`: Contém configurações e componentes de segurança.
        -   `config.py`: Gerenciamento de configurações da aplicação utilizando Pydantic.
        -   `security.py`: Implementação da segurança da API, incluindo autenticação por API Key e rate limiting.
    -   `services/`: Lógica de negócios dos serviços de IA.
        -   `language_service.py`: Serviço para detecção de idioma.
        -   `sentiment_service.py`: Serviço para análise de sentimentos.
    -   `main.py`: Ponto de entrada da aplicação FastAPI, configuração do logging, middlewares e rotas principais.
-   `tests/`: Contém testes automatizados para os endpoints da API.
    -   `test_endpoints.py`: Testes de integração para os endpoints da API.
-   `requirements.txt`: Lista de dependências Python do projeto.
-   `.env.example`: Arquivo de exemplo para variáveis de ambiente.
-   `.gitignore`: Especifica arquivos ignorados pelo Git.

## Configuração

A API utiliza variáveis de ambiente para configuração, que podem ser definidas em um arquivo `.env` na raiz do projeto. As seguintes variáveis são utilizadas:

-   `API_KEY`: Chave de API para autenticação das requisições. Valor padrão: `"default_key"`.
-   `LOG_LEVEL`: Nível de logging da aplicação. Valor padrão: `"INFO"`.
-   `ENVIRONMENT`: Ambiente da aplicação (e.g., `"development"`, `"production"`). Valor padrão: `"development"`.

Um arquivo `.env.example` é fornecido como modelo.

## Como Executar

1.  **Ambiente Virtual**: Recomenda-se criar um ambiente virtual para isolar as dependências do projeto:

    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    ```

2.  **Instalar Dependências**: Instale as dependências listadas no arquivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar API Key**: Defina uma API Key segura. Para desenvolvimento, você pode usar a chave padrão `"default_key"`, mas em produção, é crucial gerar e utilizar uma chave forte. Configure a variável de ambiente `API_KEY` no arquivo `.env` ou diretamente no ambiente do sistema.

4.  **Executar a API**: Execute a aplicação FastAPI utilizando Uvicorn:

    ```bash
    uvicorn app.main:app --reload
    ```

    O parâmetro `--reload` habilita o hot-reloading, útil durante o desenvolvimento.

5.  **Documentação da API**: Após executar a API, a documentação interativa (Swagger UI e ReDoc) estará disponível em:

    -   Swagger UI: `http://127.0.0.1:8000/docs`
    -   ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints da API

### 1. Detecção de Idioma (`/api/v1/language/detect`)

-   **Método**: `POST`
-   **Request Body**:

    ```json
    {
        "text": "Texto a ser analisado"
    }
    ```

-   **Headers**:
    -   `X-API-Key`: API Key para autenticação.
-   **Response Body**:

    ```json
    {
        "language": "Código do idioma detectado (e.g., 'en', 'pt', 'es')"
    }
    ```

-   **Exemplo de uso (curl)**:

    ```bash
    curl -X POST \
      -H "X-API-Key: sua_api_key" \
      -H "Content-Type: application/json" \
      -d '{"text": "Olá mundo"}' \
      http://127.0.0.1:8000/api/v1/language/detect
    ```

### 2. Análise de Sentimentos (`/api/v1/sentiment/analyze`)

-   **Método**: `POST`
-   **Request Body**:

    ```json
    {
        "text": "Texto a ser analisado"
    }
    ```

-   **Headers**:
    -   `X-API-Key`: API Key para autenticação.
-   **Response Body**:

    ```json
    {
        "polarity": 0.5,
        "subjectivity": 0.6,
        "sentiment": "positive" 
        // sentiment pode ser "positive", "negative" ou "neutral"
    }
    ```

-   **Exemplo de uso (curl)**:

    ```bash
    curl -X POST \
      -H "X-API-Key: sua_api_key" \
      -H "Content-Type: application/json" \
      -d '{"text": "Eu amo esta API"}' \
      http://127.0.0.1:8000/api/v1/sentiment/analyze
    ```

## Testes

Para executar os testes automatizados, utilize pytest:

```bash
pytest tests/test_endpoints.py
```

Certifique-se de ter as dependências de teste instaladas (`pytest` e `requests` em `requirements.txt`).

## Segurança

A API implementa segurança baseada em API Key e rate limiting:

-   **Autenticação por API Key**: Todas as requisições aos endpoints protegidos (`/api/v1/language/detect` e `/api/v1/sentiment/analyze`) exigem um header `X-API-Key` com uma API Key válida.
-   **Rate Limiting**: Implementado para limitar o número de requisições por IP dentro de um período de tempo, protegendo a API contra abuso e garantindo a disponibilidade do serviço. O limite padrão é de 100 requisições por hora por IP.

## Logging

A aplicação utiliza logging para registrar informações e erros. A configuração básica de logging está definida em `main.py`, registrando logs de nível INFO ou superior. Os logs são formatados com timestamp, nome do logger, nível de log e mensagem. Erros não tratados são capturados e logados globalmente.

## Próximos Passos

-   Melhorar a precisão da detecção de idioma e análise de sentimentos, possivelmente integrando modelos de IA mais avançados.
