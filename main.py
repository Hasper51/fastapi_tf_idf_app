from fastapi import FastAPI, UploadFile, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from collections import Counter
from math import log
from typing import Dict, List
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

results_storage: Dict[str, List] = {}


def compute_tf_idf(text: str) -> List[Dict]:
    """
    Calculate TF-IDF scores for words in a single document
    Returns top 50 words sorted by IDF
    """
    # Clean and prepare text
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    words = [w.lower() for w in text.split() if w.isalpha()]
    total_words = len(words)

    # Calculate TF
    tf_counts = Counter(words)
    tf = {word: count / total_words for word, count in tf_counts.items()}

    # Calculate sentence frequency for IDF
    sentence_frequency = Counter()
    for sentence in sentences:
        words_in_sentence = [w.lower() for w in sentence.split() if w.isalpha()]
        sentence_frequency.update(set(words_in_sentence))

    # Calculate IDF
    total_sentences = max(len(sentences), 1)  # prevent division by zero
    idf = {
        word: log(total_sentences / freq) for word, freq in sentence_frequency.items()
    }

    # Combine results
    result = []
    for word in tf.keys():
        result.append(
            {
                "word": word,
                "tf": tf[word],
                "idf": idf.get(word, 0),  # default to 0 if word not in idf
            }
        )

    # Sort by decreasing IDF
    result.sort(key=lambda x: x["idf"], reverse=True)
    return result[:50]


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile):
    text = await file.read()
    text = text.decode("utf-8", errors="ignore")

    session_id = str(id(request))
    results_storage[session_id] = compute_tf_idf(text)

    return RedirectResponse(f"/results?session_id={session_id}&page=1", status_code=303)


@app.get("/results", response_class=HTMLResponse)
async def paginated_results(
    request: Request, page: int = Query(1, ge=1), session_id: str = Query(...)
):
    table = results_storage.get(session_id, [])
    if not table:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "Results not found. Please upload a file first.",
            },
        )

    total_pages = (len(table) + 9) // 10
    page = min(max(1, page), total_pages)

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "words": table[start:end],
            "page": page,
            "pages": total_pages,
            "session_id": session_id,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
