# Python ka base image
FROM python:3.10-slim

# Working directory set karna
WORKDIR /app

# Requirements file copy karke dependencies install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki ka backend code copy karna
COPY . .

# FastAPI ka port expose karna
EXPOSE 8000

# Server start karne ka command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]