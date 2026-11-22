FROM python:3.11-slim
WORKDIR /app

# 1. Torch CPU wheel first, then the app deps (torch is not in requirements.deploy.txt)
COPY backend/requirements.deploy.txt backend/requirements.deploy.txt
RUN pip install --no-cache-dir torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r backend/requirements.deploy.txt

# 2. Pre-download the embedding model into the HF cache (runtime forces offline mode)
ARG EMBEDDING_MODEL=intfloat/multilingual-e5-base
ENV HF_HOME=/root/.cache/huggingface
RUN python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ.get('EMBEDDING_MODEL', '${EMBEDDING_MODEL}'))"
ENV EMBEDDING_MODEL=${EMBEDDING_MODEL}

# 3. Code and the read-only data the app needs (see .dockerignore)
COPY backend/ backend/
COPY ingestion/data/ ingestion/data/

ENV PYTHONUNBUFFERED=1
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
