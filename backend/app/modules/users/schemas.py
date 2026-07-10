from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Define a estrutura dos dados que esperamos receber ao criar um usuário.
    """
    email: EmailStr  # Valida formato de e-mail
    password: str
    name: str

class UserResponse(BaseModel):
    """
    Define a estrutura dos dados que retornamos ao consultar um usuário.
    """
    id: int
    email: str
    name: str

    class config:
        # Permite que o Pydantic leia diretamente de um objeto SQLAlchemy
        # (o model User), não só de um dicionário.
        from_attributes = True

class Token(BaseModel):
    """
    Formato de reposta do endpoint de login: o token JWT em si
    e o tipo (sempre "Bearer", padrão do protocolo de autenticação OAuth2).
    """
    access_token: str
    token_type: str = "bearer"