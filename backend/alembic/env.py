import sys
import os
import asyncio

# Garante que o Alembic encontra o pacote "app" ao rodar os comandos
sys.path.append(os.getcwd())

from app.core.config import settings          # nossas configurações (.env)
from app.db.base import Base                    # classe Base dos models
from app.modules.users.models import User       # importa o model User
from sqlalchemy.ext.asyncio import create_async_engine

# Isso "registra" o model User na metadata do SQLAlchemy,
# para o Alembic conseguir detectar a tabela automaticamente.

from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Sobrescreve a URL do banco definida no alembic.ini,
# usando a mesma URL do nosso .env (evita duplicar configuração)
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata diz ao Alembic quais tabelas existem no código Python,
# para ele comparar com o que já existe no banco e gerar a migration certa.
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Função auxiliar síncrona que configura o contexto do Alembic
    e roda as migrations. Ela é chamada de dentro de uma conexão
    assíncrona via connection.run_sync() (ver função abaixo).
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Versão assíncrona: cria um engine async (compatível com asyncpg)
    e abre uma conexão async, delegando a execução real das migrations
    para a função síncrona 'do_run_migrations' via run_sync().
    """
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # run_sync executa uma função síncrona dentro do contexto assíncrono,
        # que é exatamente o que o Alembic precisa para configurar o contexto.
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Ponto de entrada chamado no final do arquivo (modo 'online').
    Usa asyncio.run() para executar a versão assíncrona das migrations,
    já que nossa DATABASE_URL usa o driver assíncrono (asyncpg).
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()