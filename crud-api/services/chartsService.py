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

def get_charts_by_date(db: Session, query_date: date):
    """Query charts by date, joining with Song, Artist, and Genre."""
    query = db.query(
        Chart.rank_value.label('position'),
        Song.song_name.label('song'),
        Artist.artist_name.label('artist'),
        Song.song_link.label('spotify_url'),
        Song.song_length.label('duration'),
        Song.song_language.label('language'),
        Genre.genre_name.label('genre'),
        Artist.artist_gender.label('type'),
        Chart.date.label('date'),
        Chart.country_code.label('country_code'),
        Chart.source.label('source'),
        Chart.chart_type.label('chart_type')
    ).join(Song, Chart.song_id == Song.song_id) \
    .join(Artist, Chart.artist_id == Artist.artist_id) \
    .join(Genre, Artist.genre_id == Genre.genre_id) \
    .filter(Chart.date == query_date)
   
    return query


def fetch_chart_query(db: Session, year: int | None = None, date_query: date | None = None):
    """Fetch charts with optional year and date filters and return structured response."""
    try:
        if not date_query:
            date_query = date.today().strftime("%Y-%m-%d")

        query = get_charts_by_date(db, date_query)
        
        if year:
            query = query.filter(func.extract('year', Chart.date) == year)
        
        charts = query.all()
        chart_res = {}
        
        for chart in charts:
            if chart.source != "Youtube Charts" or chart.chart_type != "Daily" or chart.country_code == "GBL":
                continue
            
            country = chart.country_code
            if country not in chart_res:
                chart_res[country] = []
                
            type = chart.type

            chart_item = {
                "position": chart.position,
                "song": chart.song,
                "artist": chart.artist,
                "duration": chart.duration,
                "spotify_url": chart.spotify_url,
                "source": chart.source,
                "songFeatures": {
                    "genre": chart.genre,
                    "language": chart.language
                },
                "artistFeatures": {
                    "type": type[0].upper() + type[1:],
                    "gender": type[0].upper() + type[1:]
                }
            }
    
            if chart_item not in chart_res[country]:
                if chart.country_code == country:
                    chart_res[country].append(chart_item)
            
        response = {
            "date": str(date_query),
            "charts": chart_res
        }
        return response
    except Exception as e:
        logging.error(f"error in fetch_chart_query: {e}")
        return {}



def fetch_chart_by_id(db: Session, rank_id: uuid4):
    """Fetch a single chart by rank ID."""
    try:
        return db.query(Chart).filter(Chart.rank_id == rank_id).first()
    except NoResultFound:
        return None
  
def fetch_charts_by_available_dates(db: Session):
    """Fetch all charts and group by year, month, and day."""
    try:
        charts = db.query(Chart).all()
    except NoResultFound:
        return None
    
    try:
        grouped_data = defaultdict(lambda: defaultdict(list))
        
        for chart in charts:
            chart_date_str = chart.date.strftime("%Y-%m-%d")
            year = chart_date_str[:4]
            month = chart_date_str[5:7]
            day = chart_date_str[8:10]
            
            if day not in grouped_data[year][month]:
                grouped_data[year][month].append(day)

        return dict(grouped_data)
    except Exception as e:
        logging.error(f"Failed to fetch charts by available dates: {e}")
        return None   
    
def create_chart(db: Session, chart: ChartCreate):
    """Create a new chart and return it."""
    try:
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
    except Exception as e:
        logging.error(f"Failed to create chart: {e}")
        return None

def update_chart(db: Session, rank_id: uuid4, chart: ChartCreate):
    """Update an existing chart by rank ID and return it."""
    try:
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
    except Exception as e:
        logging.error(f"Failed to update chart: {e}")
        return None