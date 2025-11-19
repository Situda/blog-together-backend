import datetime
import math
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.models.article import Articles, ArticleSeries, ArticleCategories

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
                Articles.article_category_id
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
                Articles.article_category_id
            )
            .where(or_(Articles.article_category_id == category))
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
        .where(or_(Articles.article_category_id == category))
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
        article_category_id: Optional[int],
        series_id: int,
        session: AsyncSession,
):
    """
    创建一个文章，如果创建失败会抛出异常并终止，该异常的抛出依赖于AsyncSession.add_all()方法
    :param article_title: 文章标题
    :param article_cover: 封面URL
    :param article_abstract: 文章摘要
    :param article_content: 文章内容
    :param article_category_id: 文章所属类别id
    :param series_id: 文章所属系列id
    :param session: 会话工厂
    :return: 如果创建成功，返回True
    """
    update_time = datetime.datetime.now()
    if series_id is None:
        article = Articles(
            article_title=article_title,
            article_cover=article_cover,
            article_abstract=article_abstract,
            article_content=article_content,
            update_time=update_time,
            article_category_id=article_category_id,
        )
    else:
        article = Articles(
            article_title=article_title,
            article_cover=article_cover,
            article_abstract=article_abstract,
            article_content=article_content,
            update_time=update_time,
            article_category_id=article_category_id,
            series_id=series_id
        )
    session.add_all(
        [article, ]
    )
    await session.commit()
    return True

async def get_series_id(
        series_name: str,
        session: AsyncSession
) -> Optional[int]:
    """
    根据系列名查询系列id
    :param series_name: 系列名
    :param session: 会话工厂
    :return: 如果系列存在返回系列id，如果系列不存在或series_name为None返回None
    """
    if series_name is not None:
        stmt = (
            select(ArticleSeries.series_id)
            .where(or_(ArticleSeries.series_name == series_name))
        )
        result = await session.scalars(stmt)
        try:
            series_id = result.first()[0]
        except TypeError as e:
            raise Exception(f"series_name={series_name}，该series_name可能并不存在，因而触发异常{e}")
    else:
        series_id = None
    return series_id

async def get_category_id(
        category_name: str,
        session: AsyncSession
) -> Optional[int]:
    if category_name is not None:
        stmt = (select(ArticleCategories.article_category_id)
                .where(or_(ArticleCategories.article_category_name == category_name)))
        result = await session.scalars(stmt)
        try:
            article_category_id = result.first()[0]
        except TypeError as e:
            raise Exception(f"category_name={category_name}，该category_name可能并不存在，因而触发异常{e}")
        return article_category_id
    else:
        raise Exception("category_name不能为空")
