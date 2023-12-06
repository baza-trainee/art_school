from typing import Optional, Type

from cloudinary import uploader
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile, Response
from sqlalchemy import delete, insert, select, update, desc, func

from src.database import Base
from .schemas import SliderCreateSchema, SliderMainUpdateSchema
from .exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
    SUCCESS_DELETE,
    SLIDE_EXISTS,
    MAXIMUM_SLIDE,
)


async def get_all_slides(model: Type[Base], session: AsyncSession):
    query = select(model).order_by(model.id)
    slider = await session.execute(query)
    all_slides = slider.scalars().all()
    if not all_slides:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)

    return all_slides


async def new_slide(
    slide_data: SliderCreateSchema,
    model: Type[Base],
    session: AsyncSession,
):
    try:
        total_slides = await session.execute(select(func.count()).select_from(model))
        total_count = total_slides.scalar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)

    if total_count >= 8:
        raise HTTPException(status_code=400, detail=MAXIMUM_SLIDE)

    if slide_data.description is None:
        slide_data.description = None

    if slide_data.title is not None and isinstance(slide_data.title, str):
        query = select(model).where(func.lower(model.title) == slide_data.title.lower())
        result = await session.execute(query)
        instance = result.scalars().first()
        if instance:
            raise HTTPException(
                status_code=400,
                detail=SLIDE_EXISTS % slide_data.title,
            )
    else:
        slide_data.title = None

    photo = slide_data.photo
    folder_path = f"static/{model.__name__}"
    # os.makedirs(folder_path, exist_ok=True)
    # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
    # async with aiofiles.open(file_path, "wb") as buffer:
    #     await buffer.write(await photo.read())
    # update_data["photo"] = file_path
    try:
        upload_result = uploader.upload(photo.file, folder=folder_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="cloudinary error")

    slide_data.photo = upload_result["url"]
    try:
        query = insert(model).values(**slide_data.model_dump()).returning(model)
        result = await session.execute(query)
        slide_data = result.scalars().first()
        await session.commit()
        return slide_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_slide(
    slider_data: SliderMainUpdateSchema,
    model: Type[Base],
    session: AsyncSession,
    photo: Optional[UploadFile],
    slide_id: int,
):
    query = select(model).where(model.id == slide_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    update_data = slider_data.model_dump(exclude_none=True)
    if photo:
        folder_path = f"static/{model.__name__}"
        # os.makedirs(folder_path, exist_ok=True)
        # file_path = f"{folder_path}/{photo.filename.replace(' ', '_')}"
        # async with aiofiles.open(file_path, "wb") as buffer:
        #     await buffer.write(await photo.read())
        # update_data["photo"] = file_path
        upload_result = uploader.upload(photo.file, folder=folder_path)
        update_data["photo"] = upload_result["url"]
    if not update_data:
        return Response(status_code=204)
    try:
        query = (
            update(model)
            .where(model.id == slide_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_slide_by_id(model: Type[Base], session: AsyncSession, slide_id: int):
    query = select(model).where(model.id == slide_id)
    result = await session.execute(query)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail=NO_RECORD)

    try:
        total_slides = await session.execute(select(func.count()).select_from(model))
        total_count = total_slides.scalar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)

    if total_count == 1:
        raise HTTPException(status_code=400, detail="Cannot delete last slide")
    try:
        query = delete(model).where(model.id == slide_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % slide_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
