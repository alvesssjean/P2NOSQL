FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Chamamos o uvicorn apontando corretamente para o módulo app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]