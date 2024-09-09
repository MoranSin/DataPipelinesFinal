
---

# DataPipelinesFinalSkibidi

This is the final Skibidi project for the Data Pipelines rizz course, which showcases a complete pipeline for processing and visualizing data from various sources, including APIs, scrapers, and a Pulse application. The project features a backend API, a UI to visualize data, and automated data scrapers.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [How to Run the UI](#how-to-run-the-ui)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the API](#running-the-api)
- [Postgres Database](#postgres-database)
- [CRUD API](#crud-api)
  - [Genres](#genres)
  - [Artists](#artists)
  - [Songs](#songs)
  - [Charts](#charts)
- [Processors](#processors)
- [Pulse App](#pulse-app)
- [Scrapers](#scrapers)
  - [YouTube Scraper](#youtube-scraper)
  - [Tiktok Scraper](#tiktok-scraper)
  - [Spotify Scraper](#spotify-scraper)
- [Docker Compose Setup](#docker-compose-setup)

---

## Prerequisites

Before running the application, ensure you have the following installed:

- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Serverless Framework](https://www.serverless.com/)
- __ init __.py files inside the scrapers if does not exist yet
- .env files one for the scrapers and one for the processor

---

## Folder Structure

Here is the overall project folder structure, including all main directories and key files.
Instead of using a single `serverless.yml` file, each container (CRUD API, scrapers, processors) is modularized into its own folder with its own `serverless.yml` configuration.
This structure was chosen to improve maintainability and scalability, allowing each service (API, scraper, processor) to operate and scale separately.


```
d-----  crud-api
|         d-----  config
|         d-----  models
|         d-----  routers
|         d-----  schemas
|         d-----  services
|         -a----  app.py
|         -a----  Dockerfile
|         -a----  package-lock.json
|         -a----  package.json
|         -a----  requirements.txt
|         -a----  serverless.yml
|         -a----  __init__.py
|
d-----  postgres
|         d-----  docker-entrypoint-initdb.d
|                  -a---- init.sql
|
d-----  processor
|         d-----  MusicAddedDataAPI
|         -a----  country_code.json
|         -a----  GeniusLyricsApi.py
|         -a----  MusicBrainzApi.py
|         -a----  SpotifyApi.py
|         -a----  __init__.py
|         d-----  node_modules
|         d-----  utils
|                  -a---- dbUtils.py
|                  -a---- utils.py
|                  -a---- __init__.py
|         -a----  .env
|         -a----  Dockerfile
|         -a----  handler.py
|         -a----  package-lock.json
|         -a----  package.json
|         -a----  requirements.txt
|         -a----  serverless.yml
|
d-----  scrapers
|         d-----  spofityScraper
|         -a----  spotifyChartsDaily.py
|         -a----  spotifyChartsWeekly.py
|         -a----  spotifyScraper.py
|         -a----  __init__.py
|
|         d-----  tiktokBillboardScraper
|         -a----  tiktokScraper.py
|         -a----  __init__.py
|
|         d-----  youtubeScraper
|         -a----  youtubeChartsDaily.py
|         -a----  youtubeChartsWeekly.py
|         -a----  youtubeScraper.py
|         -a----  __init__.py
|
|         -a----  .env
|         -a----  country_code.json
|         -a----  Dockerfile
|         -a----  genericScraper.py
|         -a----  package-lock.json
|         -a----  package.json
|         -a----  requirements.txt
|         -a----  serverless.yml
|         -a----  __init__.py
|
d-----  pulse-app
|         d----- node_modules
|         d----- public
|                  -a----mockServiceWorker.js
|                  -a----vite.svg
|                  -a----worldFeatures.json
|         d----- src
|                  d-----assets
|                  d-----common
|                  d-----components
|                  d-----hooks
|                  d-----mocks
|                  d-----services
|                  d-----state
|                  -a----App.css
|                  -a----App.jsx
|                  -a----index.css
|                  -a----main.jsx
|        -a----index.html
|        -a----package-lock.json
|        -a----package.json
|        -a----README.md
|        -a----vite.config.js
-a----  docker-compose.yml
-a----  elasticmq.conf
-a----  package-lock.json
-a----  package.json
-a----  requirements.txt
```

---

## How to Run the UI

The frontend UI is built with Node.js. To set it up:

1. Change directory to the pulse-app directory:
   ```bash
   cd pulse-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

This will launch the UI.

---

## Setting Up the Environment

You will need to define environment variables for different services, including database credentials, API keys, and other configurations. These are stored in `.env` files.

Example `.env` file inside of the scraper folder:
```
YOUTUBE_CHARTS_URL_KEY= ''
YOUTUBE_CHARTS_COOKIE=''
YOUTUBE_CHARTS_API_KEY=''
YOUTUBE_TRENDS_COOKIE=''
YOUTUBE_TRENDS_API_KEY=''
SPOTIFY_API_KEY_WEEKLY=''
SPOTIFY_API_KEY_DAILY=''
```
Example `.env` file inside of the processor folder:
```
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
GENIUS_ACCESS_TOKEN = ""
```

Make sure to configure `.env` files!!!

---

## Running the API

The backend API is built using Serverless Framework and runs on a FastAPI environment.

To start the API locally:

1. Turn on the containers with Docker Compose from the root folder:
   ```bash
   docker-compose up -d
   ```
2. Automatically the scrapers will start scraping data at a designated date or time and put it into aws sqs 

3. The processor then shall take the data from the sqs add additional data through other api's and move it to the DB

3. You then may access the API at the endpoint `http://127.0.0.1:8001/dev/`.

---

## Postgres Database

This project uses PostgreSQL as its primary database. To set it up, Docker will spin up a container with a Postgres instance. The database holds information for genres, artists, songs, and charts.

Ensure that the database migrations and schema are set up before interacting with the API.

---

## CRUD API

The API provides several endpoints to manage and retrieve music-related data (genres, artists, songs, and charts). The methods allowed for each resource are as follows:

### Genres

- **Endpoint**: `http://127.0.0.1:8001/dev/genres`
- **Methods**: `GET`, `POST`

To get genre by name:
```bash
GET http://127.0.0.1:8001/dev/genres/name/{Genre_name}
```

### Artists

- **Endpoint**: `http://127.0.0.1:8001/dev/artists`
- **Methods**: `GET`, `POST`, `PATCH`

To get an artist by name:
```bash
GET http://127.0.0.1:8001/dev/artists/name/{Artist_name}
```

### Songs

- **Endpoint**: `http://127.0.0.1:8001/dev/songs`
- **Methods**: `GET`, `POST`, `PATCH`

To get a song by name:
```bash
GET http://127.0.0.1:8001/dev/songs/name/{song_name}
```

To get a song by name and artist_id:
```bash
GET http://127.0.0.1:8001/dev/songs/name/{song_name}/artist/{artist_id}
```


### Charts

- **Endpoint**: `http://127.0.0.1:8001/dev/charts`
- **Methods**: `GET`, `POST`, `PATCH`

These resources allow for the creation, retrieval, and updating of genre, artist, song, and chart data.

The GET /charts will detch the Youtube Charts daily songs from each country.

To retrieve the list of available chart dates:
```bash
GET http://127.0.0.1:8001/dev/charts/available-dates
```

## Processors

The **processors** in this project handle data processing tasks. This includes tasks like cleaning scraped data, normalizing it, and transforming it before storing it in the database.

The following API'S that are used are:

1. lyricsgenius API - Utilized to retrieve song lyrics and song language.
2. Spotify API - Utilized to obtain the artist's genre and the song's duration.
3. Musicbrainzngs API - Utilized to retrieve the artist's gender and country.

The processor is activated when the scraper sends data to the SQS queue using the `serverless` framework. It processes the information and uses FastAPI requests to insert the relevant data into the PostgreSQL database.

---

## Pulse App

The **Pulse App** is a part of the UI that visualizes real-time data, such as charts, artists, or genres. It allows users to see the data processed from scrapers and APIs.

You can access the Pulse App by running the UI and navigating to the relevant section.

---

## Scrapers

Scrapers are automated jobs that fetch data from external sources. This project includes a **YouTube Scraper**, **SpotifyScraper** and **TiktokScraper** that gathers data about songs, charts, and artists.

### YouTube Scraper

The YouTube scraper runs on scheduled intervals using the `serverless` framework and scrapes data daily or weekly, globally or by specific countries.

The data collected by the scraper is processed and stored in the aws SQS.

### Tiktok Scraper

The Tiktok scraper runs on scheduled intervals using the `serverless` framework and scrapes weekly data.

The data collected by the scraper is processed and stored in the aws SQS.

### Spotify Scraper

The Spotify scraper runs on scheduled intervals using the `serverless` framework and scrapes data daily or weekly.

The data collected by the scraper is processed and stored in the aws SQS.

---

## Docker Compose Setup

The project uses Docker Compose to run the various services (like the Postgres database) as containers.

To start the containers, use the following command:

```bash
docker-compose up -d
```

This will spin up the necessary containers for the Postgres database and any other services defined in the `docker-compose.yml` file.

To stop the containers:

```bash
docker-compose down
```

---

## Conclusion

Thank you Skibidi very much for reading. see you next year Shaked =)
This project demonstrates a complete data pipeline for music-related data using APIs, scrapers, processors, and a frontend UI. It uses PostgreSQL as a database and Docker Compose for easy setup.

For any questions or issues, feel free to open an issue on this repository.

--- 























