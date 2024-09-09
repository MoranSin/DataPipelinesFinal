FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

COPY package*.json ./

RUN npm install

EXPOSE 8001

CMD ["npx", "serverless", "offline", "--config", "serverless.yml", "--host", "0.0.0.0", "--httpPort", "8001"]
