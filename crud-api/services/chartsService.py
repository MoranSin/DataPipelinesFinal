from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.chartsModel import Chart
from schemas.chartsSchema import ChartCreate
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)

def fetch_charts(db: Session):
    return db.query(Chart).all()

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