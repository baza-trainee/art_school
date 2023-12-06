from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session

# from src.database.redis import invalidate_cache
from .models import Gallery
from .service import (
    delete_media_by_id,
    get_all_media_by_type,
    create_photo,
    create_video,
    get_media_by_id,
    update_photo,
    update_video,
)
from .schemas import (
    GetPhotoSchema,
    GetVideoSchema,
    CreatePhotoSchema,
    CreateVideoSchema,
    DeleteResponseSchema,
    PositionEnum,
)


gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])

GET_PHOTO_RESPONSE = GetPhotoSchema
GET_VIDEO_RESPONSE = GetVideoSchema
POST_PHOTO_BODY = CreatePhotoSchema
POST_VIDEO_BODY = CreateVideoSchema
DELETE_RESPONSE = DeleteResponseSchema


@gallery_router.get("/photo", response_model=Page[GET_PHOTO_RESPONSE])
async def get_all_photo(
    is_pinned: bool = None,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    result = await get_all_media_by_type(Gallery, session, is_video, is_pinned)
    disable_installed_extensions_check()
    return paginate(result)


@gallery_router.get("/video", response_model=Page[GET_VIDEO_RESPONSE])
async def get_all_video(
    session: AsyncSession = Depends(get_async_session),
):
    is_pinned = False
    is_video = True
    result = await get_all_media_by_type(Gallery, session, is_video, is_pinned)
    disable_installed_extensions_check()
    return paginate(result)


@gallery_router.get("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def get_photo(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = False
    return await get_media_by_id(Gallery, session, id, is_video)


@gallery_router.get("/video/{id}", response_model=GET_VIDEO_RESPONSE)
async def get_video(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    is_video = True
    return await get_media_by_id(Gallery, session, id, is_video)


@gallery_router.post("/photo", response_model=GET_PHOTO_RESPONSE)
async def post_photo(
    pinned_position: PositionEnum = Form(default=None),
    sub_department: int = Form(default=None),
    gallery: POST_PHOTO_BODY = Depends(POST_PHOTO_BODY.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # if sub_department:
    #    await invalidate_cache("get_gallery_for_sub_department", sub_department)
    return await create_photo(
        pinned_position, sub_department, gallery, Gallery, session
    )


@gallery_router.post("/video", response_model=GET_VIDEO_RESPONSE)
async def post_video(
    gallery: POST_VIDEO_BODY = Depends(POST_VIDEO_BODY.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await create_video(gallery, Gallery, session)


@gallery_router.patch("/photo/{id}", response_model=GET_PHOTO_RESPONSE)
async def patch_photo(
    id: int,
    pinned_position: PositionEnum = Form(default=None),
    sub_department: int = Form(default=None),
    description: str = Form(default=None, max_length=300),
    media: UploadFile = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # if sub_department:
    #     await invalidate_cache("get_gallery_for_sub_department", sub_department)
    return await update_photo(
        id, pinned_position, sub_department, description, media, Gallery, session
    )


@gallery_router.patch("/video/{id}", response_model=GET_VIDEO_RESPONSE)
async def patch_video(
    id: int,
    media: AnyHttpUrl = Form(None),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    return await update_video(id, media, Gallery, session)


@gallery_router.delete("/{id}", response_model=DELETE_RESPONSE)
async def delete_media(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # query = select(Gallery).where(Gallery.id == id, Gallery.is_video == False)
    # result = await session.execute(query)
    # if x := result.scalars().first():
    #     await invalidate_cache("get_gallery_for_sub_department", x.sub_department)
    return await delete_media_by_id(id, Gallery, session)
