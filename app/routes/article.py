from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import articles
from app.database import database
from app.services.analyze import analyze_article
from app.utils import cosine_similarity
import json

router = APIRouter()

class Article(BaseModel):
    title: str
    author: str
    content: str
    tags: list[str] = []

@router.get("")
async def get_articles():
    query = articles.select()
    rows = await database.fetch_all(query)
    result = []
    for r in rows:
        d = dict(r)
        d["tags"] = json.loads(d.get("tags", "[]"))
        result.append(d)
    return result


@router.post("/articles")
async def create_article(article: Article):
    query = articles.insert().values(
        title=article.title,
        author=article.author,
        content=article.content,
        tags=json.dumps(article.tags or [])  
    )
    last_id = await database.execute(query)
    return {**article.model_dump(), "id": last_id}

@router.get("/{id}")
async def get_article(id: int):
    query = articles.select().where(articles.c.id == id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(404, "Article not found")
    d = dict(row)
    d["tags"] = json.loads(d.get("tags", "[]"))
    return d

@router.get("/{id}/analyze")
async def analyze(id: int):
    query = articles.select().where(articles.c.id == id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(404, "Article not found")
    d = dict(row)
    d["tags"] = json.loads(d.get("tags", "[]"))
    return analyze_article(d)

@router.get("/{id1}/{id2}/analyze")
async def compare_articles(id1: int, id2: int):
    q1 = articles.select().where(articles.c.id == id1)
    q2 = articles.select().where(articles.c.id == id2)
    a1 = await database.fetch_one(q1)
    a2 = await database.fetch_one(q2)
    if not a1 or not a2:
        raise HTTPException(404, "Article not found")
    sim = cosine_similarity(a1["content"], a2["content"])
    return {"similarity": round(sim, 2)}
