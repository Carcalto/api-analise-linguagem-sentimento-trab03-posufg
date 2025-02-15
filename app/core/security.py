from fastapi import Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN, HTTP_429_TOO_MANY_REQUESTS
from .config import get_settings
import time
import logging

# Define o header esperado para a API Key. 'X-API-Key' é o nome do header que o cliente deve enviar.
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
# Dicionário para rastrear a contagem de requisições por IP do cliente para o rate limiting
request_counts = {}
# Limite de requisições permitidas dentro de um período de tempo
RATE_LIMIT = 100  # 100 requisições
RATE_TIME = 3600  # 3600 segundos = 1 hora

# Função para verificar e obter a API Key a partir do header da requisição
async def get_api_key(request: Request, api_key_header: str = Security(api_key_header)):
    # Verifica se a API Key foi fornecida no header
    if not api_key_header:
        # Se não foi fornecida, levanta uma exceção HTTP 403 (Forbidden)
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API Key não fornecida" # Mensagem de detalhe para o cliente
        )

    # Verifica se a API Key fornecida é válida comparando com a API_KEY configurada
    if api_key_header != get_settings().API_KEY:
        logging.warning(f"Tentativa de acesso com API Key inválida: {api_key_header}") # Log de aviso sobre API Key inválida
        # Se a API Key for inválida, levanta uma exceção HTTP 403 (Forbidden)
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API Key inválida" # Mensagem de detalhe para o cliente
        )

    # Implementação de Rate limiting (limite de taxa de requisições)
    client_ip = request.client.host # Obtém o IP do cliente que fez a requisição
    current_time = time.time() # Obtém o tempo atual

    # Verifica se o IP do cliente já está no dicionário de contagem de requisições
    if client_ip in request_counts:
        count, start_time = request_counts[client_ip] # Recupera a contagem e o tempo de início
        # Verifica se o período de tempo do rate limiting já expirou
        if current_time - start_time > RATE_TIME:
            request_counts[client_ip] = [1, current_time] # Reinicia a contagem para este IP
        # Verifica se o cliente excedeu o limite de requisições
        elif count >= RATE_LIMIT:
            # Se excedeu, levanta uma exceção HTTP 429 (Too Many Requests)
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisições excedido" # Mensagem de detalhe para o cliente
            )
        else:
            request_counts[client_ip][0] += 1 # Incrementa a contagem de requisições para este IP
    else:
        request_counts[client_ip] = [1, current_time] # Inicia a contagem para um novo IP

    return api_key_header # Retorna a API Key (se válida e dentro do limite de taxa)
