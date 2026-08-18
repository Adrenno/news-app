from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import (
    initialize_database,
    get_digests,
    get_article,
    get_articles,
    set_article_read_status,
)
from summarizer import summarize_article



app = FastAPI(
    title="News App API",
    description="API for the personal news digest.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()


@app.get("/")
def root():
    return {
        "message": "News App API is running."
    }


@app.get("/api/digests")
def get_all_digests(
    limit: int = 20,
    offset: int = 0,
):
    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="limit must be at least 1",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset cannot be negative",
        )

    digests = get_digests(
        limit=limit,
        offset=offset,
    )

    return {
        "digests": digests,
        "limit": limit,
        "offset": offset,
    }


@app.get("/api/digests/latest")
def get_latest_digest():
    digests = get_digests(limit=1)

    if not digests:
        return {
            "digest": None
        }

    return {
        "digest": digests[0]
    }


@app.get("/api/digests/{digest_id}")
def get_digest(digest_id: int):
    digests = get_digests(
        limit=1,
        digest_id=digest_id,
    )

    if not digests:
        raise HTTPException(
            status_code=404,
            detail="Digest not found.",
        )

    return {
        "digest": digests[0]
    }

@app.get("/api/articles")
def get_all_articles(
    limit: int = 20,
    offset: int = 0,
    category: str | None = None,
    source: str | None = None,
    search: str | None = None,
    is_read: bool | None = None,
):
    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="limit must be at least 1",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset cannot be negative",
        )

    articles = get_articles(
        limit=limit,
        offset=offset,
        category=category,
        source=source,
        search=search,
        is_read=is_read,
    )

    return {
        "articles": articles,
        "limit": limit,
        "offset": offset,
        "category": category,
        "source": source,
        "search": search,
        "is_read": is_read,
    }

@app.post("/api/articles/{article_id}/why-it-matters")
def get_why_it_matters(article_id: int):
    article = get_article(article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found.",
        )

    result = summarize_article(article)

    return {
        "article_id": article_id,
        "why_it_matters": result["why_it_matters"],
    }

@app.patch("/api/articles/{article_id}/read")
def set_article_read(
    article_id: int,
    is_read: bool,
):
    article = get_article(article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found.",
        )

    set_article_read_status(
        article_id,
        is_read,
    )

    return {
        "article_id": article_id,
        "is_read": is_read,
    }