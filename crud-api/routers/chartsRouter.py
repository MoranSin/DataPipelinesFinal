from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.chartsSchema import ChartCreate, Chart, YearDict
from schemas.responseChartsSchema import ChartResponse
from services.chartsService import fetch_chart_by_id, create_chart, update_chart, fetch_charts_by_available_dates, fetch_chart_query
from config.database import get_db
from uuid import UUID
from datetime import date

chartsRouter = APIRouter()

@chartsRouter.get("/charts", response_model=ChartResponse)
async def get_charts(db: Session = Depends(get_db),
    year: int | None = Query(default=None),
    date: date | None = Query(default=None)):
    """Retrieve charts based on year and/or date."""
    charts = fetch_chart_query(db, year, date)
    if not charts:
        raise HTTPException(status_code=404, detail="Charts not found")
    return charts 

@chartsRouter.get("/charts/available-dates", response_model=YearDict)
async def get_charts_by_available_dates(db: Session = Depends(get_db)):
    """Retrieve available dates for charts."""
    charts = fetch_charts_by_available_dates(db)
    if charts is None:
        raise HTTPException(status_code=404, detail="Charts by dates not found")
    return charts


@chartsRouter.get("/charts/{rank_id}", response_model=Chart)
async def get_chart_by_id(rank_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a single chart by its ID."""
    song = fetch_chart_by_id(db, rank_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Chart not found")
    return song

@chartsRouter.post("/charts", response_model=Chart)
async def post_chart(song: ChartCreate, db: Session = Depends(get_db)):
    """Create a new chart entry."""
    new_chart = create_chart(db, song)
    return new_chart

@chartsRouter.patch("/charts/{rank_id}", response_model=Chart)
async def patch_chart(rank_id: UUID, chart: ChartCreate, db: Session = Depends(get_db)):
    """Update an existing chart entry."""
    new_chart = update_chart(db, rank_id, chart)
    return new_chart