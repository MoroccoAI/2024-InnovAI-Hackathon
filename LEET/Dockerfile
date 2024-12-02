FROM python:3.8-slim

WORKDIR /app


RUN apt-get update \
    && apt-get install -y \
        gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .


RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000



CMD [ "bash", "-c", "tail -f /dev/null" ]
# CMD [ "python3", "app.py" ]