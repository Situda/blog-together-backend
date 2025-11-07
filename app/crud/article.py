import datetime
import math
from typing import Sequence

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_database
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
                Articles.series_id,
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
                Articles.series_id,
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

async def get_article(
        article_id: int,
        session: AsyncSession
):
    stmt = (
        select(Articles)
        .where(or_(Articles.article_id == article_id))
    )
    result = await session.scalars(stmt)
    return result.first()

async def create_article(
        article_title: str,
        article_cover: str,
        article_abstract: str,
        article_content: str,
        session: AsyncSession,
        article_category: str = None,
):
    update_time = datetime.datetime.now()
    if article_category is None:
        article = Articles(
            article_title=article_title,
            article_cover=article_cover,
            article_abstract=article_abstract,
            article_content=article_content,
            update_time=update_time,
        )
    else:
        article = Articles(
            article_title=article_title,
            article_cover=article_cover,
            article_abstract=article_abstract,
            article_content=article_content,
            update_time=update_time,
            article_category=article_category
        )
    session.add_all(
        [article, ]
    )
    await session.commit()
    return True