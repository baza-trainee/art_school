# non-business logic functions, e.g. response normalization, data enrichment, etc.
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select
from src.contacts.models import Contacts

from src.database import get_async_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan start")
    session = get_async_session()
    async for s in session:
        async with s.begin():
            query = select(Contacts)
            result = await s.execute(query)
            contacts = result.scalars().first()
            if not contacts:
                contacts = Contacts(
                    address="вул.Бульварно-Кудрявська, 2", phone="+38(097)290-79-40"
                )
                s.add(contacts)
                await s.commit()
    yield
    print("lifespan end")
