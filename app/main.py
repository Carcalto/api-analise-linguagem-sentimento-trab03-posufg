from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api.v1 import endpoints
import logging
import time

# Configuração de logging para registrar eventos e erros
logging.basicConfig(
    level=logging.INFO, # Define o nível mínimo de log para INFO (informações, avisos, erros)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' # Define o formato das mensagens de log
)

# Cria uma instância FastAPI, que é o núcleo da nossa aplicação API
app = FastAPI(
    title="IA API", # Título da API, visível na documentação
    description="API para serviços de IA: detecção de idioma e análise de sentimentos", # Descrição da API
    version="1.0.0" # Versão da API
)

# Inclui o router de endpoints da API versão 1, definindo o prefixo "/api/v1" para todas as rotas
app.include_router(endpoints.router, prefix="/api/v1")

# Middleware para adicionar um header com o tempo de processamento de cada requisição
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time() # Marca o tempo de início da requisição
    response = await call_next(request) # Processa a requisição
    process_time = time.time() - start_time # Calcula o tempo de processamento
    response.headers["X-Process-Time"] = str(process_time) # Adiciona o tempo de processamento no header da resposta
    return response # Retorna a resposta

# Handler de exceção global para capturar erros não tratados na aplicação
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Erro não tratado: {str(exc)}") # Registra o erro no log
    return JSONResponse( # Retorna uma resposta JSON de erro
        status_code=500, # Código de status HTTP 500 (Internal Server Error)
        content={"detail": "Erro interno do servidor"} # Mensagem de erro detalhada para o cliente
    )

# Rota raiz ("/") que retorna uma mensagem de boas-vindas
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de IA"} # Retorna uma mensagem JSON simples
