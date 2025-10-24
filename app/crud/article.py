import math
from typing import Sequence

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_database
from app.schemas.article import ArticleInfo, Items
from sqlalchemy import select, or_, func
from app.models.article import Articles
from loguru import logger

async def get_article_info(
        category: str,
        page: int,
        skip: int,
        session: AsyncSession
):
    if category == "all":
        stmt = (
            select(
                Articles.article_id,
                Articles.article_title,
                Articles.article_series,
                Articles.update_time,
                Articles.article_cover,
                Articles.article_category
            )
            .order_by(Articles.update_time)
            .limit(skip)
            .offset((page - 1) * skip)
        )
    else:
        stmt = (
            select(
                Articles.article_id,
                Articles.article_title,
                Articles.article_series,
                Articles.update_time,
                Articles.article_cover,
                Articles.article_category
            )
            .where(or_(Articles.article_category == category))
            .order_by(Articles.update_time)
            .limit(skip)
            .offset((page-1) * skip)
        )
    result = await session.execute(stmt)
    content = result.scalars()
    # logger.debug(content.fetchall())
    return content.fetchall()

async def get_article_info_page_count(
        category: str,
        limit: int,
        session: AsyncSession
) -> int:
    stmt = (
        select(func.count(Articles.article_id))
        .where(or_(Articles.article_category == category))
    )
    result = await session.scalars(stmt)
    total_page = max(1, math.ceil(result.first() / limit))
    return total_page