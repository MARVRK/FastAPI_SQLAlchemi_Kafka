from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from cart.infra.base import get_db

DBSessionDP= Annotated[AsyncSession, Depends(get_db)]
