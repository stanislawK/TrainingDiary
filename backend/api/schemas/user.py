from typing import Any

import strawberry
from loguru import logger
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from strawberry.types import Info

from api.models.user import User
from api.types.auth import JWTPair, LoginUserData, LoginUserError, LoginUserResponse
from api.types.general import InputValidationError
from api.utils.jwt import create_jwt_token
from api.utils.user import authenticate_user


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(
        self, info: Info[Any, Any], input: LoginUserData
    ) -> LoginUserResponse:
        # This will run pydantic's validation
        try:
            data = input.to_pydantic()
        except ValidationError as error:
            return InputValidationError(message=str(error))
        session: AsyncSession = info.context["session"]
        user = await authenticate_user(session, data.email, data.password)
        if not isinstance(user, User):
            logger.error(f"{data.email} logging failed attempt")
            return LoginUserError()
        access_token = create_jwt_token(
            subject=str(user.id), fresh=True, token_type="access"
        )
        refresh_token = create_jwt_token(
            subject=str(user.id), fresh=False, token_type="refresh"
        )
        return JWTPair(access_token=access_token, refresh_token=refresh_token)