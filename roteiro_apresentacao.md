# Roteiro de Apresentação - API de Detecção de Idioma e Análise de Sentimentos (10 minutos)

## Introdução (1 minuto)

Olá a todos! Apresentaremos nossa API de Detecção de Idioma e Análise de Sentimentos, desenvolvida como parte da disciplina "Construção de APIs para Inteligência Artificial" na UFG. O objetivo é criar uma API RESTful que ofereça esses dois serviços de IA, aplicando as boas práticas de desenvolvimento aprendidas.

## Contexto e Motivação (1 minuto)

Este projeto foi desenvolvido por Célio Carcalto e Anahi Philbois. A motivação por trás deste projeto é a crescente necessidade de processamento de linguagem natural em diversas aplicações, desde chatbots até análise de feedback de clientes. A detecção de idioma e a análise de sentimentos são componentes fundamentais nesse processo.

## Demonstração da API (4 minutos)

Vamos demonstrar a funcionalidade da API. Ela possui dois endpoints principais:

1.  **Detecção de Idioma:**
    *   A detecção de idioma utiliza a biblioteca `langdetect`, que analisa estatisticamente o texto para identificar padrões característicos de cada idioma, como sequências de caracteres e frequência de palavras. Com base nessa análise, a API retorna o código ISO 639-1 do idioma mais provável.
    *   Vamos enviar um texto em português: "Olá, mundo!".
    *   A API deve retornar "pt" (código ISO 639-1 para português).
    *   Agora, um texto em inglês: "Hello, world!".
    *   A API deve retornar "en".
    *   Testaremos com um texto inválido/vazio para demonstrar o tratamento de erros.

2.  **Análise de Sentimentos:** *Observação: Atualmente, a análise de sentimentos suporta apenas o idioma inglês.*
    *   A análise de sentimentos é feita com a biblioteca `TextBlob`, que utiliza um léxico (dicionário de palavras) com scores de polaridade e subjetividade associados a cada palavra. O texto é analisado, e a polaridade e subjetividade geral são calculadas.
    *   Enviaremos um texto positivo: "This movie is excellent!".
    *   A API deve retornar um sentimento "positivo" com scores de polaridade e subjetividade.
    *   Um texto negativo: "The service was terrible.".
    *   A API deve retornar "negativo".
    *   Um texto neutro: "The sky is blue.".
    *   A API deve retornar "neutro".
    *   Testaremos com um texto em idioma não suportado para demonstrar o tratamento de erros.

(Demonstrar os endpoints usando um cliente REST como Insomnia ou Postman, ou via Swagger UI/ReDoc).

## Aspectos Técnicos (3 minutos)

A API foi construída com FastAPI, um framework moderno e de alta performance para APIs em Python. Implementamos as seguintes boas práticas:

*   **Validação de dados:** Usamos a biblioteca Pydantic para definir modelos de dados (schemas) que validam automaticamente os dados de entrada das requisições. Se os dados não corresponderem ao schema, a API retorna um erro antes mesmo de processar a requisição. Os modelos estão em `app/services/language_service.py` e `app/services/sentiment_service.py`.
*   **Tratamento de erros:** Implementamos um tratamento de erros customizado. Capturamos exceções que podem ocorrer durante o processamento das requisições (como texto vazio ou erros de análise) e retornamos respostas de erro HTTP apropriadas com mensagens informativas. Isso está implementado nos arquivos de serviço (`app/services/language_service.py` e `app/services/sentiment_service.py`) e em `app/main.py` para erros mais genéricos.
*   **Logs:** Utilizamos o módulo `logging` do Python para registrar eventos importantes, como requisições recebidas, erros e informações de depuração. Isso facilita o rastreamento de problemas e o monitoramento da API. A configuração do logging está em `app/main.py`. *Atualmente, os logs são exibidos no console (saída de erro padrão), pois não foi especificado um arquivo para armazená-los.*
*   **Segurança:** A API requer que cada requisição inclua um cabeçalho `X-API-Key` com uma chave de API válida. Isso garante que apenas usuários autorizados possam acessar os endpoints. *Para usar a API, é necessário fornecer essa chave no cabeçalho de cada requisição. A chave pode ser configurada no arquivo `.env` (variável `API_KEY`) ou diretamente como variável de ambiente do sistema.* Além disso, implementamos *rate limiting* para limitar o número de requisições por IP, protegendo contra abusos. *O rate limiting restringe o número de requisições que um cliente pode fazer em um determinado período. No nosso caso, o limite é de 100 requisições por hora por IP.* A lógica de segurança está em `app/core/security.py`.
*   **Versionamento:** A API possui um versionamento explícito (v1) no caminho dos endpoints (`/api/v1/...`). Isso permite que futuras versões da API sejam lançadas sem afetar os clientes que usam a versão antiga. Os endpoints da versão 1 estão em `app/api/v1/endpoints.py`.
*   **Documentação:** A API é auto-documentada. O FastAPI gera automaticamente uma documentação interativa (Swagger UI e ReDoc) com base nos modelos de dados e nas definições dos endpoints. Isso facilita o uso e a integração da API. A configuração do FastAPI, incluindo a geração da documentação, está em `app/main.py`.

*   **Testes:** Implementamos testes automatizados usando a biblioteca `pytest`. Os testes lêem frases de um arquivo de texto (`tests/test_phrases.txt`), fazem requisições à API e verificam se os resultados correspondem às expectativas. Isso garante a qualidade e a confiabilidade da API.

## Conclusão (1 minuto)

Esta API demonstra a aplicação prática dos conceitos aprendidos na disciplina. Ela é funcional, bem documentada, segura e segue as boas práticas de desenvolvimento. O código está disponível no GitHub e pronto para ser executado e testado. *Gostaríamos de enfatizar que, no momento, a análise de sentimentos é limitada ao inglês, mas planejamos expandir o suporte para incluir o português do Brasil em futuras iterações.* Agradecemos a atenção!
