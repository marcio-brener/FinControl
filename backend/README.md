# FinControl

Aplicação de controle financeiro pessoal, desenvolvida como projeto de estudo com foco em arquitetura backend robusta e boas práticas de mercado.

## Sobre o projeto

O FinControl permite registrar receitas e despesas, acompanhar saldo e visualizar a movimentação financeira através de gráficos. É um projeto multiusuário, onde cada usuário tem seus dados isolados e protegidos por autenticação.

Este projeto foi criado com dois objetivos principais:
- Ter uma ferramenta pessoal de controle financeiro
- Aprofundar conhecimentos em arquitetura de software, APIs REST, autenticação e desenvolvimento full stack

## Tecnologias

**Backend**
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic (migrations)
- JWT (autenticação)
- Docker

**Frontend**
- React + TypeScript
- Vite
- (em desenvolvimento)

## Status do projeto

🚧 Em desenvolvimento — MVP em construção.

## Roadmap

- [x] Setup do backend (FastAPI + PostgreSQL + Docker)
- [x] Cadastro e autenticação de usuários (JWT)
- [ ] CRUD de transações
- [ ] Proteção de rotas por usuário autenticado
- [ ] Dashboard com gráficos
- [ ] Frontend em React
- [ ] Categorias e contas múltiplas
- [ ] Deploy