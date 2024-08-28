# DataPipelinesFinalSkibidi
final project for data pipelines course

# skibid how to run the UI
1.npm install

2.npm run dev

# Turn on the containers with docker-compose
docker-compose up -d

# The API:
http://127.0.0.1:8001/dev/

## have the resources:
### Genres:
http://127.0.0.1:8001/dev/genres
methods allowed: GET, POST.

#### Get genre by name
http://127.0.0.1:8001/dev/genres/name/{Genre_name}

### Artists:
http://127.0.0.1:8001/dev/artists
methods allowed: GET, POST, PATCH.

#### Get Artist by name
http://127.0.0.1:8001/dev/artists/name/{Artist_name}

### Songs:
http://127.0.0.1:8001/dev/songs
methods allowed: GET, POST, PATCH.

#### Get Song by name
http://127.0.0.1:8001/dev/songs/name/{Song_name}

### Charts:
http://127.0.0.1:8001/dev/charts
methods allowed: GET, POST, PATCH.

### Invoking scheduler functions

```bash
    serverless invoke local --function youtubeScraperWeekly
```

```bash
    serverless invoke local --function youtubeScraperDaily
```