FROM python:3.12.10-slim

#для healthcheck
RUN apt-get update  \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /file_upload

# Оптимизация пересборки проекта в случаях когда библиотеки не изменились
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8030

CMD ["python3", "main.py"]