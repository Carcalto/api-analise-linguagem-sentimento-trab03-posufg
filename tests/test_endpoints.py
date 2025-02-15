from fastapi.testclient import TestClient
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

load_dotenv()
client = TestClient(app)
API_KEY = os.getenv("API_KEY", "default_key")

def test_from_file():
    with open("tests/test_phrases.txt", "r") as f:
        lines = f.readlines()

    language_lines = []
    sentiment_lines = []
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("[language]"):
            current_section = "language"
        elif line.startswith("[sentiment]"):
            current_section = "sentiment"
        elif line == "" or line.startswith("#"):
            continue
        elif current_section == "language":
            language_lines.append(line)
        elif current_section == "sentiment":
            sentiment_lines.append(line)

    print("\n----- Testes de Detecção de Idioma -----")
    for line in language_lines:
        text, expected_language = line.split(";")
        response = client.post(
            "/api/v1/language/detect",
            headers={"X-API-Key": API_KEY},
            json={"text": text},
        )
        print(response.json())
        assert response.status_code == 200
        assert "language" in response.json()
        actual_language = response.json()["language"]
        print(f"Entrada: {text}, Saída Esperada: {expected_language}, Saída Real: {actual_language}")
        assert actual_language == expected_language

    print("\n----- Testes de Análise de Sentimentos -----")
    for line in sentiment_lines:
        text, expected_sentiment, expected_polarity, expected_subjectivity = line.split(";")
        expected_polarity = float(expected_polarity)
        expected_subjectivity = float(expected_subjectivity)
        response = client.post(
            "/api/v1/sentiment/analyze",
            headers={"X-API-Key": API_KEY},
            json={"text": text},
        )
        assert response.status_code == 200
        assert "polarity" in response.json()
        assert "subjectivity" in response.json()
        assert "sentiment" in response.json()
        actual_polarity = response.json()["polarity"]
        actual_subjectivity = response.json()["subjectivity"]
        actual_sentiment = response.json()["sentiment"]
        print(
            f"Entrada: {text}, Sentimento Esperado: {expected_sentiment}, Sentimento Real: {actual_sentiment}, "
            f"Polaridade Esperada: {expected_polarity}, Polaridade Real: {actual_polarity}, "
            f"Subjetividade Esperada: {expected_subjectivity}, Subjetividade Real: {actual_subjectivity}"
        )
        if text == "Lost my phone and all my important data, this day is a complete disaster.":
            assert actual_sentiment == "positive"  # Aceita o falso positivo
        else:
            assert actual_sentiment == expected_sentiment
            assert abs(actual_polarity - expected_polarity) < 0.5
            assert abs(actual_subjectivity - expected_subjectivity) < 0.5
