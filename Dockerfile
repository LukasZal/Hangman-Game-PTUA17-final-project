FROM python:3.13-slim

WORKDIR /app/hangman

COPY app/ /app/hangman

RUN mkdir -p /app/hangman/logs

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
