# Python ka base image
FROM python:3.10-slim

# Working directory set karna
WORKDIR /app

# Requirements file copy karke dependencies install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki ka frontend code copy karna
COPY . .

# Streamlit ka port expose karna
EXPOSE 8501

# App start karne ka command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]