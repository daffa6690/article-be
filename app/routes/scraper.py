from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import articles
from app.services.scraper import scrape_detik
import json

router = APIRouter()


@router.post("/scrape_url")
async def scrape_url(url: str):
    try:
        data = scrape_detik(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    query = articles.insert().values(
        title=data["title"],
        author=data["author"],
        date=data["date"],
        content=data["content"],
        tags=json.dumps(data.get("tags", [])),
    )
    last_id = await database.execute(query)
    return {**data, "id": last_id}
