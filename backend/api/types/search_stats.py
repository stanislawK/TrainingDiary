from datetime import datetime, timedelta
from typing import Annotated, List, Optional, Union

import strawberry
from sqlmodel.ext.asyncio.session import AsyncSession

from api.models.search import Search
from api.types.category import CategoryType, convert_category_from_db
from api.types.event_stats import EventStatsType
from api.types.general import Error
from api.utils.search import get_search_events_for_search, get_search_stats


@strawberry.input
class SearchStatsInput:
    id: int
    date_from: Optional[datetime] = strawberry.UNSET
    date_to: Optional[datetime] = strawberry.UNSET


@strawberry.experimental.pydantic.type(Search)
class SearchStatsType:
    date_from: datetime
    date_to: datetime
    category: CategoryType
    location: strawberry.auto
    distance_radius: strawberry.auto
    from_price: strawberry.auto
    to_price: strawberry.auto
    from_surface: strawberry.auto
    to_surface: strawberry.auto
    avg_price_total: float
    avg_price_per_square_meter_total: float
    avg_area_total: Optional[float] = strawberry.UNSET
    avg_terrain_total: Optional[float] = strawberry.UNSET
    events: List[EventStatsType]


async def convert_search_stats_from_db(
    session: AsyncSession,
    search: Search,
    date_from: datetime = datetime.utcnow() - timedelta(days=365),
    date_to: datetime = datetime.utcnow(),
) -> SearchStatsType:
    search_events = await get_search_events_for_search(
        session=session, search=search, date_from=date_from, date_to=date_to
    )
    search_stats = get_search_stats(search_events)
    return SearchStatsType(
        date_from=date_from,
        date_to=date_to,
        category=convert_category_from_db(search.category),  # type: ignore
        location=search.location,
        distance_radius=search.distance_radius,
        from_price=search.from_price,
        to_price=search.to_price,
        from_surface=search.from_surface,
        to_surface=search.to_surface,
        avg_price_total=search_stats.get("avg_price_total"),
        avg_price_per_square_meter_total=search_stats.get(
            "avg_price_per_square_meter_total"
        ),
        avg_area_total=search_stats.get("avg_area_total"),
        avg_terrain_total=search_stats.get("avg_terrain_total"),
        events=search_events,
    )


@strawberry.type
class SearchDoesntExistError(Error):
    message: str = "Search with provided id doesn't exist"


GetSearchStatsResponse = Annotated[
    Union[SearchStatsType, SearchDoesntExistError],
    strawberry.union("GetSearchStatsResponse"),
]