# Základní Python image
FROM python:3.13-slim

# Nastavení pracovního adresáře v kontejneru
WORKDIR /app

# Nechceme .pyc soubory a chceme nebufferovaný výstup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Nejdřív závislosti
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pak zbytek aplikace
COPY . .

# Defaultní příkaz – async varianta
CMD ["python", "-m", "app.async_main"]
