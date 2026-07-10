from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserResponse, Token
from app.core.security import hash_password, verify_password, create_access_token

# APIRouter agrupa endpoints relacionados (aqui, tudo sobre "users").
# O main.py vai "incluir" esse router na aplicação principal.
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo usuário.
    - Recebe UserCreate (email, password, name) já validado pelo Pydantic.
    - Verifica se o e-mail já existe antes de criar (evita duplicidade).
    - Nunca salva a senha em texto puro — só o hash.
    """
    # Verifica se já existe um usuário com esse e-mail
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    # Cria o novo usuário com a senha já em hash
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        name=user_data.name,
    )

    db.add(new_user)          # marca o objeto para ser inserido
    await db.commit()          # efetiva a inserção no banco
    await db.refresh(new_user) # atualiza new_user com dados gerados pelo banco (ex: id)

    return new_user  # o Pydantic converte automaticamente para UserResponse


@router.post("/login", response_model=Token)
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Autentica um usuário existente.
    - Busca o usuário pelo e-mail.
    - Compara a senha enviada com o hash salvo no banco.
    - Se bater, gera e retorna um token JWT.
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    # Mensagem de erro genérica de propósito: não dizemos se foi o e-mail
    # ou a senha que errou, para não dar dica a quem está tentando invadir.
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos",
    )

    if not user:
        raise credentials_error

    if not verify_password(password, user.hashed_password):
        raise credentials_error

    # Gera o token contendo o id do usuário (usaremos isso depois
    # para identificar "quem" está fazendo cada requisição autenticada)
    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=access_token)