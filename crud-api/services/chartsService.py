from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.chartsModel import Chart
from models.songsModel import Song
from models.artistsModel import Artist
from models.genreModel import Genre
from schemas.chartsSchema import ChartCreate
from uuid import uuid4
import logging
from datetime import date

logging.basicConfig(level=logging.INFO)

def fetch_charts(db: Session):
    return db.query(Chart).all()

def fetch_chart_query(db: Session, year: int | None = None, date_query: date | None = None):
    try:
        query = db.query(
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
            .join(Genre, Artist.genre_id == Genre.genre_id)
        
        if year:
            query = query.filter(func.extract('year', Chart.date) == year)
        
        if date_query:
            query = query.filter(Chart.date == date_query)

        charts = query.all()
        result = {}
        for chart in charts:
            date_str = chart.date.isoformat()
            country_code_key = chart.country_code

            if date_str not in result:
                result[date_str] = {}

            if country_code_key not in result[date_str]:
                result[date_str][country_code_key] = set() 

            chart_data_tuple = (
                chart.position,
                chart.song,
                chart.artist,
                chart.duration,
                chart.spotify_url,
                chart.genre,
                "English", 
                chart.gender,
                chart.source  
            )

            result[date_str][country_code_key].add(chart_data_tuple)

        final_result = [
            {
                "date": date,
                "charts": {
                    country_code: sorted(
                        [
                            {
                                "position": entry[0],
                                "song": entry[1],
                                "artist": entry[2],
                                "duration": entry[3],
                                "spotify_url": entry[4],
                                "source": entry[8],  # Add source to the entry
                                "songFeatures": {
                                    "genre": entry[5],
                                    "language": entry[6],
                                },
                                "artistFeatures": {
                                    "gender": entry[7],
                                },
                            }
                            for entry in country_code_data
                        ],
                        key=lambda x: x["position"]
                    )
                    for country_code, country_code_data in country_code_data.items()
                }
            }
            for date, country_code_data in result.items()
        ]

        print(f"this is final result {final_result}")
        print(type(final_result))
        print(type(result))

        return final_result
    except Exception as e:
        print(f"error in fetch_chart_query: {e}")
        return []



def fetch_chart_by_id(db: Session, rank_id: uuid4):
    try:
        return db.query(Chart).filter(Chart.rank_id == rank_id).first()
    except NoResultFound:
        return None
  
def fetch_charts_by_available_dates(db: Session):
    try:
        charts = db.query(Chart).all()
    except NoResultFound:
        return None
    
    grouped_data = defaultdict(lambda: defaultdict(list))
    
    for chart in charts:
        chart_date_str = chart.date.strftime("%Y-%m-%d")
        year = chart_date_str[:4]
        month = chart_date_str[5:7]
        day = chart_date_str[8:10]
        
        if day not in grouped_data[year][month]:
            grouped_data[year][month].append(day)

    return dict(grouped_data)
    
    
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