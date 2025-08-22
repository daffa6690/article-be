from sqlalchemy import Table, Column, Integer, String, Text
from app.database import metadata

articles = Table (
    'articles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('author', String, nullable=False),
    Column("date", String, nullable=False),
    Column('content', Text, nullable=False),
    Column('tags', Text, nullable=True, default='[]')
)