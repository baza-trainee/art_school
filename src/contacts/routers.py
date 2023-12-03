from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from fastapi_cache.decorator import cache

# from src.config import HOUR, MONTH
from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.contacts.service import delete_record, get_record, update_record
from src.database import get_async_session

# from src.redis import invalidate_cache, my_key_builder
from .schemas import ContactField, ContactsSchema, ContactsUpdateSchema
from .models import Contacts


router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=ContactsSchema)
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_contacts(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_record(Contacts, session)


@router.patch("", response_model=ContactsSchema)
async def update_contacts(
    contacts_update: ContactsUpdateSchema = Depends(ContactsUpdateSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_contacts")
    return await update_record(contacts_update, Contacts, session)


@router.delete("/{field}", response_model=ContactsSchema)
async def clear_field(
    field: ContactField,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_contacts")
    return await delete_record(field, Contacts, session)
