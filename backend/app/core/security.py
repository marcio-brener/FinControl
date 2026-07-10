from enum import verify
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# CryptContext é a ferramenta que gera hashes de senhas (tipo bcrypt).
# bcrypt é um algoritmo seguro e padrão da indústria.
# gera um "salt" automático, então a mesma senha nunca gera um mesmo hash.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Criptografa a senha
def hash_password(password: str) -> str:
    """
    Recebe a senha em texto puro e retorna o hash para salvar no banco.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Recebe a senha em texto puro e o hash salvo no banco e retorna True se baterem.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Cria o token JWT (Access Token).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    # Assina o token com a SECRET_KEY — só quem tem essa chave
    # consegue gerar um token válido ou verificar um token existente.
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
