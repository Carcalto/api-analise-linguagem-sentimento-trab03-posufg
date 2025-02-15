from textblob import TextBlob # Importa a biblioteca TextBlob para análise de sentimentos
from pydantic import BaseModel, validator # Importa BaseModel e validator do Pydantic para validação de dados
import logging # Importa logging para registrar logs de eventos

# Define o modelo de requisição para análise de sentimentos
class SentimentRequest(BaseModel):
    text: str # Campo 'text' obrigatório, do tipo string, que representa o texto a ser analisado

    # Validador para garantir que o texto não esteja vazio
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip(): # Remove espaços em branco do início e fim e verifica se está vazio
            raise ValueError('O texto não pode estar vazio') # Levanta um ValueError se o texto estiver vazio
        return v # Retorna o texto validado

    class Config:
        schema_extra = { # Configuração para exemplos no schema da documentação da API
            "example": {
                "text": "I love this API" # Exemplo de texto para requisição de análise de sentimento
            }
        }

# Define o modelo de resposta para análise de sentimentos
class SentimentResponse(BaseModel):
    polarity: float # Campo 'polarity' do tipo float, representa a polaridade do sentimento (-1.0 a 1.0)
    subjectivity: float # Campo 'subjectivity' do tipo float, representa a subjetividade do texto (0.0 a 1.0)
    sentiment: str # Campo 'sentiment' do tipo string, representa a classificação geral do sentimento (positivo, negativo, neutro)

    class Config:
        schema_extra = { # Configuração para exemplos no schema da documentação da API
            "example": {
                "polarity": 0.5, # Exemplo de valor de polaridade
                "subjectivity": 0.5, # Exemplo de valor de subjetividade
                "sentiment": "positive" # Exemplo de classificação de sentimento (positivo)
            }
        }

# Função para classificar o sentimento com base no valor da polaridade
def classify_sentiment(polarity: float) -> str:
    """Classifica o sentimento com base na polaridade.
    Valores de polaridade próximos a 1 indicam sentimento positivo, próximos a -1 indicam negativo, e próximos a 0 indicam neutro.
    """
    if polarity > 0.2: # Se a polaridade for maior que 0.2, considera como positivo
        return "positive"
    elif polarity < -0.2: # Se a polaridade for menor que -0.2, considera como negativo
        return "negative"
    else: # Caso contrário (entre -0.2 e 0.2), considera como neutro
        return "neutral"

# Função principal para analisar o sentimento de um texto
def analyze_sentiment(text: str) -> dict:
    """
    Analisa o sentimento do texto fornecido.

    Args:
        text: Texto para análise

    Returns:
        Dicionário contendo polaridade, subjetividade e sentimento.
    """
    try:
        analysis = TextBlob(text) # Cria um objeto TextBlob para realizar a análise do texto
        polarity = round(analysis.sentiment.polarity, 2) # Extrai e arredonda a polaridade do sentimento para 2 casas decimais
        subjectivity = round(analysis.sentiment.subjectivity, 2) # Extrai e arredonda a subjetividade para 2 casas decimais
        sentiment = classify_sentiment(polarity) # Classifica o sentimento com base na polaridade
        return { # Retorna um dicionário com os resultados da análise
            "polarity": polarity, # Polaridade do sentimento
            "subjectivity": subjectivity, # Subjetividade do texto
            "sentiment": sentiment # Classificação do sentimento (positivo, negativo, neutro)
        }
    except Exception as e: # Captura exceções genéricas que possam ocorrer durante a análise
        logging.error(f"Erro na análise de sentimento: {str(e)}") # Registra o erro no log
        return { # Em caso de erro, retorna um dicionário com valores neutros/zerados
            "polarity": 0.0, # Polaridade neutra (0.0)
            "subjectivity": 0.0, # Subjetividade nula (0.0)
            "sentiment": "neutral" # Sentimento classificado como neutro
        }
