from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import Gallery
from .service import (
    delete_media_by_id,
    get_all_media_by_filter,
    create_photo,
    create_video,
    get_photo_by_id,
    get_positions_status,
    get_video_by_id,
    update_photo_by_id,
    update_video_by_id,
)
from .schemas import (
    GetPhotoSchema,
    GetTakenPositionsSchema,
    GetVideoSchema,
    CreatePhotoSchema,
    UpdatePhotoSchema,
    DeleteResponseSchema,
)

# from src.database.redis import invalidate_cache

gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])


@gallery_router.get("/photo", response_model=Page[GetPhotoSchema])
async def get_all_photo(
    is_pinned: bool = None,
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_media_by_filter(
        is_pinned=is_pinned, reverse=reverse, is_video=False, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@gallery_router.get("/video", response_model=Page[GetVideoSchema])
async def get_all_video(
    reverse: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_all_media_by_filter(
        is_pinned=False, reverse=reverse, is_video=True, session=session
    )
    disable_installed_extensions_check()
    return paginate(record)


@gallery_router.get("/photo/{id}", response_model=GetPhotoSchema)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_photo_by_id(id=id, session=session)


@gallery_router.get("/positions", response_model=GetTakenPositionsSchema)
async def get_positions(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_positions_status(session=session)


@gallery_router.get("/video/{id}", response_model=GetVideoSchema)
async def get_video(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_video_by_id(id=id, session=session)


@gallery_router.post("/photo", response_model=GetPhotoSchema)
async def post_photo(
    schema: CreatePhotoSchema = Depends(CreatePhotoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await create_photo(schema=schema, session=session)
    # if record.sub_department:
    #    await invalidate_cache("get_gallery_for_sub_department", record.sub_department)

    return record


@gallery_router.post("/video", response_model=GetVideoSchema)
async def post_video(
    media: AnyHttpUrl,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_video(media=media, session=session)


@gallery_router.put("/photo/{id}", response_model=GetPhotoSchema)
async def put_photo(
    id: int,
    background_tasks: BackgroundTasks,
    schema: UpdatePhotoSchema = Depends(UpdatePhotoSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record: Gallery = await update_photo_by_id(
        id=id,
        schema=schema,
        session=session,
        background_tasks=background_tasks,
    )
    # if record.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", record.sub_department)
    return record


@gallery_router.put("/video/{id}", response_model=GetVideoSchema)
async def put_video(
    id: int,
    media: AnyHttpUrl,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_video_by_id(id=id, media=media, session=session)


@gallery_router.delete("/{id}", response_model=DeleteResponseSchema)
async def delete_media(
    id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # record: Gallery = await session.get(Gallery, id)
    # if record.sub_department:
    #     await invalidate_cache("get_achievement_for_sub_department", record.sub_department)
    return await delete_media_by_id(
        id=id, background_tasks=background_tasks, session=session
    )
