FROM python:3.12-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"] 