from pydantic import config
from pydantic_settings import BaseSettings

#BaseSettings é uma classe que nos ajuda a carregar variáveis do ambiente (.env).

class Settings(BaseSettings):
    database_url: str                         # URL com o PostgreSQL (vem do .env)
    secret_key: str                           # Chave secreta para assinar tokens JWT
    algorithm: str = "HS256"                  # Algoritmo de assinatura do JWT (valor padrão)
    access_token_expire_minutes: int = 60     # Tempo de expiração do token JWT (padrão 60 min)

    class Config:
        env_file = ".env"                     # Diz ao Pydantic onde buscar as variáveis do ambiente (.env)

# Instancia única (singleton) das configurações.
# Em vez de ler o .env toda vez, importamos "settings" pronto em qualquer lugar do app.
settings = Settings()