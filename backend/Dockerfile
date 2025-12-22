FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_chatbot/ ./rag_chatbot/

EXPOSE 7860

CMD ["uvicorn", "rag_chatbot.main:app", "--host", "0.0.0.0", "--port", "7860"]
