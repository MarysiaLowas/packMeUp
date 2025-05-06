from fastapi import HTTPException
from fastapi_sqlalchemy import async_db as db
from sqlalchemy import delete, exists, select
from sqlalchemy.dialects.postgresql import insert
from starlette.status import HTTP_404_NOT_FOUND


class CrudMixin:

    @classmethod
    async def exists(cls, **kwargs):
        stmt = exists(select(cls).filter_by(**kwargs)).select()
        obj_exists: bool = await db.session.scalar(stmt)
        if not obj_exists:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=f"{cls.__name__} matching {kwargs} doesn't exist"
            )
        return obj_exists

    @classmethod
    async def create(cls, **kwargs):
        stmt = insert(cls).values(kwargs).returning("*")
        result = await db.session.execute(stmt)
        return result.one()

    @classmethod
    async def merge(cls, key: list[str], /, data: list | dict):
        stmt = insert(cls).values(data)
        stmt = stmt.on_conflict_do_update(index_elements=key, set_=stmt.excluded)
        result = await db.session.execute(stmt.returning("*"))
        return result.all()

    @classmethod
    async def get(cls, **kwargs):
        statement = select(cls).filter_by(**kwargs)
        obj = (await db.session.execute(statement)).unique().scalars().one_or_none()
        if not obj:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=f"{cls.__name__} matching {kwargs} doesn't exist"
            )

        return obj

    @classmethod
    async def select(cls, **kwargs):
        statement = select(cls).filter_by(**kwargs)
        objs = (await db.session.execute(statement)).scalars().all()
        return objs

    @classmethod
    async def delete(cls, **kwargs):
        stmt = delete(cls).filter_by(**kwargs).returning("*")
        result = await db.session.execute(stmt)
        return result.all()
