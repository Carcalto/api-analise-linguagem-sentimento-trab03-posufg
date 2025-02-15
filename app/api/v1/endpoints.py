from fastapi import APIRouter, Depends
from ...core.security import get_api_key
from ...services.language_service import TextRequest, LanguageResponse, detect_language
from ...services.sentiment_service import SentimentRequest, SentimentResponse, analyze_sentiment

# Cria um APIRouter para definir os endpoints da API versão 1
router = APIRouter()

# Endpoint para detecção de idioma
@router.post("/language/detect", response_model=LanguageResponse)
async def detect_text_language(
    request: TextRequest, # Request body contendo o texto a ser analisado
    api_key: str = Depends(get_api_key) # Dependência para verificar a API key
):
    """
    Endpoint para detectar o idioma do texto fornecido.

    - Recebe um texto como input.
    - Utiliza o serviço de detecção de idioma para identificar o idioma.
    - Retorna o idioma detectado.
    """
    language = detect_language(request.text) # Chama o serviço de detecção de idioma
    return LanguageResponse(language=language) # Retorna a resposta com o idioma detectado

# Endpoint para análise de sentimentos
@router.post("/sentiment/analyze", response_model=SentimentResponse)
async def analyze_text_sentiment(
    request: SentimentRequest, # Request body contendo o texto a ser analisado
    api_key: str = Depends(get_api_key) # Dependência para verificar a API key
):
    """
    Endpoint para analisar o sentimento do texto fornecido.

    - Recebe um texto como input.
    - Utiliza o serviço de análise de sentimentos para determinar o sentimento (positivo, negativo, neutro).
    - Retorna o resultado da análise de sentimento.
    """
    result = analyze_sentiment(request.text) # Chama o serviço de análise de sentimentos
    return SentimentResponse(**result) # Retorna a resposta com o resultado da análise de sentimento
