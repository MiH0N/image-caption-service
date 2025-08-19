# Basic FastAPI Project

## Installation

1. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 