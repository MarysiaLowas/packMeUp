from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

from fastapi import HTTPException
from fastapi_sqlalchemy import async_db as db  # type: ignore
from sqlalchemy import delete, exists, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import Select
from starlette.status import HTTP_404_NOT_FOUND

T = TypeVar("T", bound="CrudMixin")


class CrudMixin:
    @classmethod
    async def exists(cls: Type[T], **kwargs: Any) -> bool:
        stmt = exists(select(cls).filter_by(**kwargs)).select()
        obj_exists: bool = await db.session.scalar(stmt)
        if not obj_exists:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"{cls.__name__} matching {kwargs} doesn't exist",
            )
        return obj_exists

    @classmethod
    async def create(cls: Type[T], **kwargs: Any) -> T:
        stmt = insert(cls).values(kwargs).returning("*")
        result = await db.session.execute(stmt)
        return cast(T, result.one()[0])

    @classmethod
    async def merge(
        cls: Type[T],
        key: List[str],
        /,
        data: Union[List[Dict[str, Any]], Dict[str, Any]],
    ) -> List[T]:
        stmt = insert(cls).values(data)
        stmt = stmt.on_conflict_do_update(index_elements=key, set_=stmt.excluded)
        result = await db.session.execute(stmt.returning("*"))
        return [cast(T, row[0]) for row in result.all()]

    @classmethod
    async def get(cls: Type[T], **kwargs: Any) -> T:
        statement = select(cls).filter_by(**kwargs)
        obj = (await db.session.execute(statement)).unique().scalars().one_or_none()
        if not obj:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"{cls.__name__} matching {kwargs} doesn't exist",
            )

        return cast(T, obj)

    @classmethod
    async def select(cls: Type[T], **kwargs: Any) -> List[T]:
        statement = select(cls).filter_by(**kwargs)
        objs = (await db.session.execute(statement)).scalars().all()
        return cast(List[T], objs)

    @classmethod
    async def select_one(cls: Type[T], statement: Select) -> Optional[T]:
        """Execute a custom select query and return a single result.

        Args:
            statement: SQLAlchemy select statement

        Returns:
            Single result or None if no results
        """
        result = await db.session.execute(statement)
        return cast(Optional[T], result.unique().scalar_one_or_none())

    @classmethod
    async def delete(cls: Type[T], **kwargs: Any) -> List[T]:
        stmt = delete(cls).filter_by(**kwargs).returning("*")
        result = await db.session.execute(stmt)
        return [cast(T, row[0]) for row in result.all()]
