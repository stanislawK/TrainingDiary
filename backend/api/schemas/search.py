from datetime import datetime, timedelta
from typing import Any

import strawberry
from strawberry.types import Info

from api.permissions import IsAuthenticated
from api.types.search_stats import (
    AssignSearchInput,
    AssignSearchResponse,
    GetSearchesResponse,
    GetSearchStatsResponse,
    NoSearchesAvailableError,
    SearchAssignSuccessfully,
    SearchDoesntExistError,
    SearchStatsInput,
    convert_search_stats_from_db,
    convert_searches_from_db,
)
from api.utils.search import get_search_by_id, get_searches


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore
    async def search_stats(
        self, info: Info[Any, Any], input: SearchStatsInput
    ) -> GetSearchStatsResponse:
        session = info.context["session"]
        search = await get_search_by_id(session, input.id)
        if not search:
            return SearchDoesntExistError()
        date_from = input.date_from or datetime.utcnow() - timedelta(days=365)
        date_to = input.date_to or datetime.utcnow()
        return await convert_search_stats_from_db(session, search, date_from, date_to)

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore
    async def all_searches(self, info: Info[Any, Any]) -> GetSearchesResponse:
        session = info.context["session"]
        searches_db = await get_searches(session=session)
        if len(searches_db) == 0:
            return NoSearchesAvailableError()
        return convert_searches_from_db(searches_db)

    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore
    async def users_searches(self, info: Info[Any, Any]) -> GetSearchesResponse:
        session = info.context["session"]
        user = info.context["request"].state.user
        searches_db = await get_searches(session=session, user_id=user.id)
        if len(searches_db) == 0:
            return NoSearchesAvailableError()
        return convert_searches_from_db(searches_db)


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])  # type: ignore
    async def assign_search_to_user(
        self, info: Info[Any, Any], input: AssignSearchInput
    ) -> AssignSearchResponse:
        session = info.context["session"]
        search = await get_search_by_id(session, input.id)
        if not search:
            return SearchDoesntExistError()
        user = info.context["request"].state.user
        if user not in search.users:
            search.users.append(user)
            session.add(search)
            await session.commit()
        return SearchAssignSuccessfully()
