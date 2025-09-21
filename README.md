# CobrejaApp - Django Ninja

Projeto criado para estudar e aprofundar conhecimentos no framework Django Ninja, baseado em Django.
Também serve como referência de arquitetura de projeto para consultas futuras.

Além disso, o projeto explora o conceito de multi-tenancy, onde:

- Um token do tenant é enviado via header da requisição (X-TOKEN).
- Esse token é usado para consultar o Redis e recuperar as informações de acesso do tenant, incluindo dados de banco de dados.
- Com isso, é possível conectar dinamicamente ao banco correto para cada tenant.

para rodar a migrate para todos, será necessário rodar o comando `uv run manage.py migrate_tenants`

# Comandos rápidos

- `uv sync` - instala dependencias
- `uv run manage.py makemigrations` - verifica se existe novas models para migrar
- `uv run manage.py migrate` - roda a migration a nivel local
- `uv run manage.py migrate_tenants` - inicia migrate a nivel do mult tenant, irei controlar via redis

- `uv run pytest -v` - roda os testes
- `uv run manage.py runserver` - inicia a app a nivel local
