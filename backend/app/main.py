from fastapi import FastAPI
from app.modules.users.router import router as users_router

# Cria a instância principal da aplicação.
# "title" aparece na documentção automática do Swagger/OpenAPI.
app = FastAPI(title="FinControl API")

# Registra todos os endpoints definidos em users/router.py
# sob o prefixo /users (ex: POST /users/register, POST /users/login)
app.include_router(users_router)

# Endpoint simples só pra confirmar que o servidor está rodando.
# GET /health > retorna um JSON simples { "status": "ok"}
@app.get("/health")
async def health_check():
    return {"status": "ok"}