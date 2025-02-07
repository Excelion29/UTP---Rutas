from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from database.models.users import UserDB
from database.models.oauth_acces_token import AccessTokenDB
from database.models.oauth_refresh_tokens import RefreshTokenDB
from database.models.transport_modes import TransportModesDB
from database.models.vehicles import VechiclesDB
from database.models.routes import RoutesDB
from database.models.assigned_routes import AssignedRoutesDB
from database.models.travel_summary import TravelSummaryDB
from database.models.roles import RolesDB
from database.models.users_roles import UserRolesDB
from database.models.permissions import PermissionsDB
from database.models.users_permissions import UserPermissionsDB
from database.models.roles_permissions import RolesPermissionsDB


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = UserDB.metadata
target_metadata = AccessTokenDB.metadata
target_metadata = RefreshTokenDB.metadata
target_metadata = TransportModesDB.metadata
target_metadata = VechiclesDB.metadata
target_metadata = RoutesDB.metadata
target_metadata = AssignedRoutesDB.metadata
target_metadata = TravelSummaryDB.metadata
target_metadata = RolesDB.metadata
target_metadata = UserRolesDB.metadata
target_metadata = PermissionsDB.metadata
target_metadata = UserPermissionsDB.metadata
target_metadata = RolesPermissionsDB.metadata

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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
