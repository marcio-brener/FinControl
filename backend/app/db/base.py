from sqlalchemy.orm import DeclarativeBase

# Base é a classe "mãe" de todas as tabelas do banco.
# Toda vez que criamos um model novo (ex: User, Transaction), 
# ele vai herdar de Case oara o SQLAlchemy saber que é uma tabela.
class Base(DeclarativeBase):
    pass