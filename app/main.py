from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import article, scraper
from app.database import database, engine, metadata
from contextlib import asynccontextmanager

metadata.create_all(engine)

@asynccontextmanager
async def lifespan (app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    
app = FastAPI(title='Article Management API', lifespan=lifespan)

app.include_router(article.router, prefix='/articles', tags=['Articles'])
app.include_router(scraper.router, tags=['Scraper'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)