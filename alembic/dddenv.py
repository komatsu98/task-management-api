from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings
from app.db.base import Base

# Determine environment type
IS_TEST_ENV = "test" in settings.ENV

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# Set the database URL dynamically
config.set_main_option("sqlalchemy.url", settings.DATABASE_URI)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        batch_mode=IS_TEST_ENV
        and "sqlite"
        in settings.DATABASE_URI,  # ✅ Enable batch only in test SQLite,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Enable batch mode only for test environment with SQLite
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "named"},
            batch_mode=IS_TEST_ENV
            and "sqlite"
            in settings.DATABASE_URI,  # ✅ Enable batch only in test SQLite,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
