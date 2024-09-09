from pydantic import BaseModel, validator, RootModel
from uuid import UUID, uuid4
from datetime import date
from typing import Dict, List

class Chart(BaseModel):
    """Model for a chart with all required attributes."""
    rank_id: UUID
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str

    class Config:
        """Configuration to enable attribute-based instantiation."""
        from_attributes = True

class ChartCreate(BaseModel):
    """Model for creating a chart."""
    artist_id: UUID
    song_id: UUID
    rank_value : int
    date : date
    source : str
    country_code : str
    chart_type : str


class DayList(RootModel[List[str]]):
    """Model for a list of days as strings."""
    pass

class MonthDict(RootModel[Dict[str, DayList]]):
    """Model for a dictionary of months, each containing a DayList."""
    pass

class YearDict(RootModel[Dict[str, MonthDict]]):
    """Model for a dictionary of years, each containing a MonthDict."""
    pass
