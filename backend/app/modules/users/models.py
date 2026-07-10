from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base 

# User herda de Base, então o SQLAlchemy sabe que essa classe representa uma tabela no banco de dados.
class User(Base):
    __tablename__ = 'users'  # Nome da tabela no Postgres
    
    # Mapped[int] diz o tipo Python; mapped_column configura a coluna no banco
    # primary_key=True define que essa coluna é a chave primária (indicador único de cada usuário)
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # unique=True impede que dois usuários tenham o mesmo e-mail
    # index=True cria um índice no banco para buscas rápidas
    email: Mapped[str] = mapped_column(unique=True, index=True)

    # O hash da senha é gerado no security.py.
    hashed_password: Mapped[str]

    # Nome de exibição do usuário.
    name: Mapped[str]