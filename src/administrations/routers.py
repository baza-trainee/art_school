from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

# from fastapi_cache.decorator import cache

# from src.config import HOUR, MONTH
from src.administrations.service import (
    create_administration,
    delete_administration,
    get_all_administration,
    get_one_administrator,
    update_administration,
)
from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session

# from src.database.redis import invalidate_cache, my_key_builder
from .models import SchoolAdministration
from .schemas import (
    AdministratorSchema,
    AdministratorCreateSchema,
    AdministratorUpdateSchema,
    DeleteResponseSchema,
)


school_admin_router = APIRouter(
    prefix="/school_administration", tags=["School Administration"]
)


@school_admin_router.get("", response_model=List[AdministratorSchema])
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_all_school_administration(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_administration(SchoolAdministration, session)


@school_admin_router.post("", response_model=AdministratorSchema)
async def create_school_administration(
    person: AdministratorCreateSchema = Depends(AdministratorCreateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_all_school_administration")
    return await create_administration(person, SchoolAdministration, session)


@school_admin_router.get("/{id}", response_model=AdministratorSchema)
async def get_school_administration(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_one_administrator(id, SchoolAdministration, session)


@school_admin_router.patch("/{id}", response_model=AdministratorSchema)
async def update_school_administration(
    id: int,
    photo: Annotated[UploadFile, File()] = None,
    person: AdministratorUpdateSchema = Depends(AdministratorUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_all_school_administration")
    return await update_administration(id, person, photo, SchoolAdministration, session)


@school_admin_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_school_administration(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_all_school_administration")
    return await delete_administration(id, SchoolAdministration, session)
