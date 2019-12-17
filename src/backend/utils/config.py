import os

from utils.database_url import DatabaseURL


POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'postgres')
POSTGRES_USER = os.getenv("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", 'postgres')
POSTGRES_DB = os.getenv("POSTGRES_DB", 'postgres')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5432')
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
# SQLALCHEMY_DATABASE_URI: DatabaseURL = DatabaseURL(
#     drivername="postgresql+psycopg2",
#     username=POSTGRES_USER,
#     password=POSTGRES_PASSWORD,
#     host=POSTGRES_HOST,
#     port=POSTGRES_PORT,
#     database=POSTGRES_DB,
# )
ALEMBIC_CONFIG: DatabaseURL = DatabaseURL(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)
