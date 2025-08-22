import databases
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./articles.db"

database = databases.Database(DATABASE_URL)


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata = MetaData()
