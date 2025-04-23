# TF-IDF Text Analysis Web Application

A web application built with FastAPI that analyzes text documents using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm.

## Features

- Upload text files for analysis
- Calculate TF-IDF scores for words in the document
- Display top 50 words sorted by IDF score
- Paginated results (10 items per page)
- Simple and intuitive web interface

## Technical Stack

- Python 3.x
- FastAPI
- Jinja2 Templates
- Uvicorn (ASGI server)
- Poetry (dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi_tf_idf_app
```

2 Install Poetry (if not installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
For Windows PowerShell:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

## Running the Application

1. Activate the Poetry virtual environment:
```bash
poetry shell
```

2. Start the application:
```bash
poetry run python main.py
```
Or using uvicorn directly:
```bash
poetry run uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`


## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000`
2. Upload a text file using the provided form
3. View the TF-IDF analysis results, paginated with 10 words per page
4. Navigate through pages using the pagination controls

## API Endpoints

- `GET /`: Main page with upload form
- `POST /upload`: Endpoint for file upload and processing
- `GET /results`: View paginated results (query parameters: `session_id`, `page`)

## How it Works

The application:
1. Processes uploaded text files
2. Splits text into sentences and words
3. Calculates Term Frequency (TF) for each word
4. Calculates Inverse Document Frequency (IDF) using sentence frequency
5. Combines TF and IDF scores
6. Returns top 50 words sorted by IDF score
