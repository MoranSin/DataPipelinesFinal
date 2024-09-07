from pydantic import BaseModel, validator, RootModel
from uuid import UUID, uuid4
from datetime import date
from typing import Dict, List

class Chart(BaseModel):
    rank_id: UUID
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str

    class Config:
        from_attributes = True

class ChartCreate(BaseModel):
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str


class DayList(RootModel[List[str]]):
    pass

class MonthDict(RootModel[Dict[str, DayList]]):
    pass

class YearDict(RootModel[Dict[str, MonthDict]]):
    pass
