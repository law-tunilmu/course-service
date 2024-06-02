import os
import httpx
import dotenv
from enum import Enum

from fastapi import status, Header
from fastapi import HTTPException

from .exceptions import CourseException

from pydantic import BaseModel

class USER_ROLES(Enum):
    STUDENT="STUDENT"
    MENTOR="MENTOR"


class User(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True

async def authorize(authorization: str | None = Header(default=None)) -> User:
    if not authorization:
        raise CourseException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            description="Authorization token is missing"
        )
    dotenv.load_dotenv()

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                os.environ["AUTH_BE"] + "/users/me",
                headers={
                    "Authorization": authorization
                }
            )

            if resp.status_code >= 500:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            elif resp.status_code >= 400:
                raise CourseException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    description="Authorization error: invalid token"
                )
            else:
                return User.model_validate(resp.json())
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

