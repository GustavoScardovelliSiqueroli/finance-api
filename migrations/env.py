# type: ignore
import importlib
import pkgutil
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import src.domain.models  # Importa o pacote principal onde estão os modelos
from src.config import Config
from src.domain.models.base import Base  # 🚀 Importa a Base corretamente
import inspect

# Garante que todos os módulos dentro de `models` sejam importados
for _, module_name, _ in pkgutil.iter_modules(src.domain.models.__path__):
    module = importlib.import_module(f'src.domain.models.{module_name}')
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, src.domain.models.base.Base):
            globals()[name] = obj  # Torna a classe acessível globalmente

# Obtém a configuração do Alembic
config = context.config
config.set_main_option('sqlalchemy.url', Config().get_db_url_alembic())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🚀 Usa Base.metadata para garantir que todos os modelos sejam reconhecidos
target_metadata = Base.metadata  # ✅ Correção principal aqui!
print(target_metadata.tables.keys())
# --------------------------------------------
# Função para rodar migrações no modo offline
# --------------------------------------------
def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()

# --------------------------------------------
# Função para rodar migrações no modo online
# --------------------------------------------
def run_migrations_online() -> None:
    """Executa migrações no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# --------------------------------------------
# Decide o modo de execução (online/offline)
# --------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
