from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.crud.article import get_article_info, get_article_info_page_count, get_article
from app.database import get_database
from typing import Annotated
from app.api_responser import TodoResponse, OKResponse, ErrorResponse

router = APIRouter(
    prefix="/articles",
    tags=["文章与系列查询"],
    responses={404: {"description": "Not found"}}
)

@router.get("",summary="分页查询文章/系列信息")
async def articles_by_category(
        category: Annotated[str, Query(max_length=30)] = "all",
        is_series: bool = False,
        skip: Annotated[int, Path(title="skip", ge=1)] = 1,
        limit: Annotated[int, Path(title="limit", ge=1)] = 9,
        session: AsyncSession = Depends(get_database)
) -> JSONResponse:
    """
    获取全部文章
    :param category: 文章category，可选，默认"all"，表示查询所有文章
    :param is_series: 系列文章过滤器，True表示只返回系列文章的入口信息，False表示返回单个文章和系列文章的信息，默认False
    :param skip: 文章分页时的第几页，默认1
    :param limit: 每页的返回文章信息数量，默认9
    :param session:
    :return: 一个包含文章信息的列表，列表的每个元素是一个如下的JSON:
            ```
            {
                "info": {
                    "page": 当前页数,
                    "total_page": 总页数
                }
                "article_list": 文章列表
            }
            其中，"article_list"是一个文章列表，其每个元素为如下JSON:
            {
                article_id: 文章id,
                article_title: 文章标题,
                article_series: 文章所属系列的id，可能为空,
                update_time: 文章更新日期,
                article_cover: 文章封面的URL,
                article_category: 文章所属category的id,
            }
            ```
    """
    # logger.debug(items.limit)
    if is_series:
        return TodoResponse()
    else:
        try:
            content = {
                "info": {
                    "page": skip,
                    "total_page": await get_article_info_page_count(category, limit, session)
                },
                "article_list": await get_article_info(category, skip, limit, session)
            }
            return OKResponse(content=content)
        except Exception as e:
            logger.error(e)
            return ErrorResponse(e)


@router.get("/{article_id}", summary="查询文章信息")
async def article_by_id(
        article_id: Annotated[int, Path(title="article_id")],
        session: AsyncSession = Depends(get_database)
):
    """
    根据id获取某一文章的全部信息
    :param article_id: 文章的id
    :param session: 会话工厂
    :return: 文章的完整信息Json，文章不存在或查询失败会返回404错误码和错误信息
            ```
            {
                "article_id": 文章id,
                "article_title": 文章标题,
                "article_series": 文章所属系列的id，可能为空,
                "update_time": 文章更新日期,
                "article_cover": 文章封面的URL,
                "article_abstract": 文章摘要（Markdown）,
                "article_content": 文章正文（Markdown）,
                "article_category": 文章所属category的id
            }
            ```
    """
    try:
        content = await get_article(article_id=article_id, session=session)
        if not content:
            raise HTTPException(status_code=404, detail=f"数据库中没有article_id = {article_id}的文章/系列")
        return OKResponse(content=content)
    except Exception as e:
        logger.error(e)
        return ErrorResponse(e)

@router.get("/categories", summary="待实现")
async def article_categories():
    """
    获取所有category的列表
    :return: 一个列表，其每个元素的值为如下
            ```
            {
                "article_category_id": 文章category的id
                "article_category_name": 文章category的名称
            }
            ```
    """
    return

@router.get("/series/{series_id}", summary="待实现")
async def series_by_id(series_id: int):
    """
    TODO: 未来实现，通过series_id查询系列
    :param series_id:
    :return: TODO: 未来实现，文章系列的信息
    """
    pass