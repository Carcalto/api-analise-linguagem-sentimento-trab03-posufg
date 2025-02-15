from fastapi.testclient import TestClient # Importa TestClient para criar um cliente de teste para a API
import sys # Importa sys para manipulação de paths do sistema
import os # Importa os para interagir com o sistema operacional
import logging # Importa logging para registrar logs
from dotenv import load_dotenv # Importa load_dotenv para carregar variáveis de ambiente do arquivo .env
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Adiciona o diretório pai ao path para importar módulos da aplicação
from app.main import app # Importa a instância FastAPI 'app' do main.py

load_dotenv() # Carrega variáveis de ambiente do arquivo .env
client = TestClient(app) # Cria um cliente de teste para a aplicação FastAPI
API_KEY = os.getenv("API_KEY", "default_key") # Obtém a API Key das variáveis de ambiente, usando 'default_key' como fallback

from fastapi.testclient import TestClient
import sys
import os
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

load_dotenv()
client = TestClient(app)
API_KEY = os.getenv("API_KEY", "default_key")

# Teste para o endpoint de detecção de idioma
def test_detect_language():
    # Texto em inglês para teste
    text = "This is a longer text in English, to improve language detection accuracy."
    expected_language = "en" # Idioma esperado: inglês
    # Faz uma requisição POST para o endpoint de detecção de idioma
    response = client.post(
        "/api/v1/language/detect", # Endpoint para detecção de idioma
        headers={"X-API-Key": API_KEY}, # Header com a API Key
        json={"text": text} # Corpo da requisição em JSON, contendo o texto
    )
    actual_language = response.json()["language"] # Extrai o idioma detectado da resposta JSON
    print(f"Entrada: {text}, Saída Esperada: {expected_language}, Saída Real: {actual_language}") # Imprime os resultados para debug
    assert response.status_code == 200 # Verifica se o status code da resposta é 200 (OK)
    assert "language" in response.json() # Verifica se a chave 'language' está presente na resposta JSON
    assert actual_language == expected_language # Verifica se o idioma detectado é igual ao idioma esperado

# Teste para detecção de idioma em português
def test_detect_language_portuguese():
    text = "Olá mundo" # Texto em português
    expected_language = "pt" # Idioma esperado: português
    response = client.post(
        "/api/v1/language/detect",
        headers={"X-API-Key": API_KEY},
        json={"text": text}
    )
    actual_language = response.json()["language"]
    print(f"Entrada: {text}, Saída Esperada: {expected_language}, Saída Real: {actual_language}")
    assert response.status_code == 200
    assert "language" in response.json()
    assert actual_language == expected_language

# Teste para detecção de idioma em espanhol
def test_detect_language_spanish():
    text = "Hola mundo" # Texto em espanhol
    expected_language = "es" # Idioma esperado: espanhol
    response = client.post(
        "/api/v1/language/detect",
        headers={"X-API-Key": API_KEY},
        json={"text": text}
    )
    actual_language = response.json()["language"]
    print(f"Entrada: {text}, Saída Esperada: {expected_language}, Saída Real: {actual_language}")
    assert response.status_code == 200
    assert "language" in response.json()
    assert actual_language == expected_language

# Teste para análise de sentimento com texto positivo
def test_analyze_sentiment():
    text = "I love this API" # Texto positivo
    expected_polarity = 0.5 # Polaridade esperada (valor positivo)
    expected_subjectivity = 0.6 # Subjetividade esperada
    expected_sentiment = "positive" # Sentimento esperado: positivo
    response = client.post(
        "/api/v1/sentiment/analyze", # Endpoint para análise de sentimento
        headers={"X-API-Key": API_KEY}, # Header com a API Key
        json={"text": text} # Corpo da requisição em JSON, contendo o texto
    )
    actual_polarity = response.json()["polarity"] # Extrai a polaridade da resposta JSON
    actual_subjectivity = response.json()["subjectivity"] # Extrai a subjetividade da resposta JSON
    actual_sentiment = response.json()["sentiment"] # Extrai o sentimento classificado da resposta JSON
    print(f"Entrada: {text}, Polaridade Esperada: {expected_polarity}, Polaridade Real: {actual_polarity}, Subjetividade Esperada: {expected_subjectivity}, Subjetividade Real: {actual_subjectivity}, Sentimento Esperado: {expected_sentiment}, Sentimento Real: {actual_sentiment}") # Imprime resultados para debug
    assert response.status_code == 200 # Verifica se o status code é 200 (OK)
    assert "polarity" in response.json() # Verifica se a chave 'polarity' está na resposta JSON
    assert "subjectivity" in response.json() # Verifica se a chave 'subjectivity' está na resposta JSON
    assert "sentiment" in response.json() # Verifica se a chave 'sentiment' está na resposta JSON
    assert response.json()["polarity"] > 0.2 # Verifica se a polaridade é maior que 0.2 (indicando sentimento positivo)
    assert response.json()["subjectivity"] > 0.2 # Verifica se a subjetividade é maior que 0.2
    assert actual_sentiment == expected_sentiment # Verifica se o sentimento classificado é igual ao esperado

# Teste para análise de sentimento com texto negativo
def test_analyze_sentiment_negative():
    text = "I hate this API" # Texto negativo
    expected_polarity = -0.8 # Polaridade esperada (valor negativo)
    expected_subjectivity = 0.9 # Subjetividade esperada
    expected_sentiment = "negative" # Sentimento esperado: negativo
    response = client.post(
        "/api/v1/sentiment/analyze",
        headers={"X-API-Key": API_KEY},
        json={"text": text}
    )
    actual_polarity = response.json()["polarity"]
    actual_subjectivity = response.json()["subjectivity"]
    actual_sentiment = response.json()["sentiment"]
    print(f"Entrada: {text}, Polaridade Esperada: {expected_polarity}, Polaridade Real: {actual_polarity}, Subjetividade Esperada: {expected_subjectivity}, Subjetividade Real: {actual_subjectivity}, Sentimento Esperado: {expected_sentiment}, Sentimento Real: {actual_sentiment}")
    assert response.status_code == 200
    assert "polarity" in response.json()
    assert "subjectivity" in response.json()
    assert "sentiment" in response.json()
    assert response.json()["polarity"] < -0.2 # Verifica se a polaridade é menor que -0.2 (indicando sentimento negativo)
    assert response.json()["subjectivity"] > 0.2
    assert actual_sentiment == expected_sentiment

# Teste para análise de sentimento com texto neutro
def test_analyze_sentiment_neutral():
    text = "This is an API" # Texto neutro
    expected_polarity = 0.0 # Polaridade esperada (valor neutro)
    expected_subjectivity = 0.0 # Subjetividade esperada (baixa para textos factuais)
    expected_sentiment = "neutral" # Sentimento esperado: neutro
    response = client.post(
        "/api/v1/sentiment/analyze",
        headers={"X-API-Key": API_KEY},
        json={"text": text}
    )
    actual_polarity = response.json()["polarity"]
    actual_subjectivity = response.json()["subjectivity"]
    actual_sentiment = response.json()["sentiment"]
    print(f"Entrada: {text}, Polaridade Esperada: {expected_polarity}, Polaridade Real: {actual_polarity}, Subjetividade Esperada: {expected_subjectivity}, Subjetividade Real: {actual_subjectivity}, Sentimento Esperado: {expected_sentiment}, Sentimento Real: {actual_sentiment}")
    assert response.status_code == 200
    assert "polarity" in response.json()
    assert "subjectivity" in response.json()
    assert "sentiment" in response.json()
    assert -0.2 <= response.json()["polarity"] <= 0.2 # Verifica se a polaridade está dentro da faixa de neutro
    assert response.json()["subjectivity"] < 0.5 # Verifica se a subjetividade é baixa
    assert actual_sentiment == expected_sentiment # Verifica se o sentimento classificado é igual ao esperado
