from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.chartsModel import Chart
from models.songsModel import Song
from models.artistsModel import Artist
from models.genreModel import Genre
from schemas.chartsSchema import ChartCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_charts(db: Session):
    return db.query(Chart).all()

def fetch_chart_query(db: Session):
    charts = db.query(
        Chart.rank_id.label('rank_id'),
        Chart.rank_value.label('position'),
        Song.song_name.label('song'),
        Artist.artist_name.label('artist'),
        Song.song_link.label('spotify_url'),
        Song.song_length.label('duration'),
        Genre.genre_name.label('genre'),
        Artist.artist_gender.label('gender'),
        Chart.date.label('date'),
        Chart.country_code.label('country_code'),
        Chart.source.label('source'),
        Chart.chart_type.label('chart_type')
    ).join(Song, Chart.song_id == Song.song_id) \
     .join(Artist, Chart.artist_id == Artist.artist_id) \
     .join(Genre, Artist.genre_id == Genre.genre_id) \
     .all()

    result = {}

    for chart in charts:
        date_str = chart.date.isoformat()
        source_type_key = f"{chart.source}_{chart.chart_type}"

        if date_str not in result:
            result[date_str] = {}

        if source_type_key not in result[date_str]:
            result[date_str][source_type_key] = []

        chart_data = {
            "position": chart.position,
            "song": chart.song,
            "artist": chart.artist,
            "duration": chart.duration,
            "spotify_url": chart.spotify_url,
            "songFeatures": {
                "genre": chart.genre,
                "language": "English",  # Example static value, adjust if needed
            },
            "artistFeatures": {
                "gender": chart.gender,
            },
        }

        result[date_str][source_type_key].append(chart_data)

    return [
        {
            "date": date,
            "charts": source_type_data
        }
        for date, source_type_data in result.items()
    ]



def fetch_chart_by_id(db: Session, rank_id: uuid4):
    try:
        return db.query(Chart).filter(Chart.rank_id == rank_id).first()
    except NoResultFound:
        return None
    
def create_chart(db: Session, chart: ChartCreate):

    new_chart = Chart(
        rank_id = uuid4(),
        artist_id = chart.artist_id,
        song_id = chart.song_id,
        rank_value = chart.rank_value,
        date = chart.date,
        source = chart.source,
        country_code = chart.country_code,
        chart_type = chart.chart_type

    )
    db.add(new_chart)
    db.commit()
    db.refresh(new_chart)
    return new_chart

def update_chart(db: Session, rank_id: uuid4, chart: ChartCreate):
    db_chart = db.query(Chart).filter(Chart.rank_id == rank_id).first()
    db_chart.artist_id = chart.artist_id
    db_chart.song_id = chart.song_id
    db_chart.rank_value = chart.rank_value
    db_chart.date = chart.date
    db_chart.source = chart.source
    db_chart.country_code = chart.country_code
    db_chart.chart_type = chart.chart_type
    db.commit()
    db.refresh(db_chart)
    return db_chart