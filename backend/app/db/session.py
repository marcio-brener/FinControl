from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# engine = motor de conexão com o banco, configurado de forma assíncrona.
# echo=True faz o SQLAlchemy imprimir no teminal cada query SQL executada
# (ótimno para aprender/debugar, depois pode desligar em produção)
engine = create_async_engine(settings.database_url, echo=True)

# async_session é uma "fábrica" que cria sessões de banco sob demanda.
# expire_on_commit=False evita que os objetos "expirem" automaticamente
# depois de salvar, o que causaria erros ap tentare ler os dados em seguida.
async_session = async_sessionmaker(engine, expire_on_commit=False)

# get_db é uma "dependency" do FastAPI: cada rota que precisar do banco 
# vai receber uma sessão nova, e ela é fechada automaticamente no final
# da requisição, evitando vazamento de conexões.
async def get_db():
    async with async_session() as session:
        yield session