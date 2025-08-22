import requests
from bs4 import BeautifulSoup

def scrape_detik(url: str) -> dict:
    if "detik.com" not in url:
        raise ValueError("Only detik.com URLs are supported")

    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        raise ValueError(f"Failed to fetch the URL (status {resp.status_code})")

    soup = BeautifulSoup(resp.text, "html.parser")

    
    title_tag = soup.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    
    author_node = soup.select_one(".detail__author, .author")
    if author_node:
        author_text = author_node.get_text(strip=True)
        if "-" in author_text:
            author = author_text.split("-")[0].strip()   
        else:
            author = author_text.strip()
    else:
        author = "Unknown"

    date_node = soup.select_one(".detail__date, .date")
    date = date_node.get_text(strip=True) if date_node else "Unknown"
    
    content_nodes = (
        soup.select(".detail__body-text p") or
        soup.select(".artikel__body p") or
        soup.select(".read__content p") or
        soup.select("article p")
    )
    content = "\n".join(p.get_text(strip=True) for p in content_nodes)

    tag_nodes = soup.select(".detail__body-tag a")
    tags = [a.get_text(strip=True) for a in tag_nodes]

    return {
        "title": title,
        "author": author,
        "date": date,
        "content": content,
        "tags": tags
    }
