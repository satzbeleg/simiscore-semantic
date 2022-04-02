FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# download sentence-transformers model
RUN mkdir -p /sbert-models
ENV SENTENCE_TRANSFORMERS_HOME=/sbert-models
RUN python3 -c 'import sentence_transformers as sbert; sbert.SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2");'

COPY ./app /app/app
