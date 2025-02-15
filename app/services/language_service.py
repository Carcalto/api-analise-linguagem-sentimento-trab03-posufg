from langdetect import detect, LangDetectException # Importa funções da biblioteca langdetect para detecção de idioma
from pydantic import BaseModel, validator # Importa BaseModel e validator do Pydantic para validação de dados
import logging # Importa logging para registrar logs de eventos

# Define o modelo de requisição para detecção de idioma
class TextRequest(BaseModel):
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
                "text": "Hello world" # Exemplo de texto para requisição
            }
        }

# Define o modelo de resposta para detecção de idioma
class LanguageResponse(BaseModel):
    language: str # Campo 'language' do tipo string, que representa o idioma detectado (código ISO)

    class Config:
        schema_extra = { # Configuração para exemplos no schema da documentação da API
            "example": {
                "language": "en" # Exemplo de código de idioma (inglês) na resposta
            }
        }

# Função para detectar o idioma de um texto
def detect_language(text: str) -> str:
    """
    Detecta o idioma do texto fornecido.

    Args:
        text: Texto para análise

    Returns:
        Código ISO do idioma detectado
    """
    try:
        if len(text.strip()) < 3: # Se o texto após remover espaços em branco for menor que 3 caracteres
            return "unknown" # Retorna 'unknown' pois textos muito curtos podem ser difíceis de detectar
        return detect(text) # Utiliza a função detect da biblioteca langdetect para detectar o idioma
    except LangDetectException: # Captura exceção específica da biblioteca langdetect
        return "unknown" # Retorna 'unknown' em caso de falha na detecção
    except Exception as e: # Captura outras exceções genéricas
        logging.error(f"Erro na detecção de idioma: {str(e)}") # Registra o erro no log
        return "unknown" # Retorna 'unknown' em caso de erro
