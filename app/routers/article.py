from fastapi import APIRouter
from app.schemas.article import Items

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def articles_by_category(items: Items):
    """
    获取全部文章
    :param items:
        ```
        {
            category: 文章category，可选，默认"all"，表示查询所有文章
            is_series: 系列文章过滤器，True表示只返回系列文章的入口信息，False表示返回单个文章和系列文章的信息，默认False
            page: 文章分页时的第几页，默认1
            limit: 每页的返回文章信息数量，默认9
        }
        ```
    :return: 一个包含文章信息的列表，列表的每个元素是一个如下的JSON:
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
                article_name: 文章标题,
                article_series: 文章所属系列的id，可能为空,
                update_time: 文章更新日期,
                article_cover: 文章封面的URL,
                article_category: 文章所属category的id,
            }
    """
    ret = None
    if items.is_series:
        return
    else:
        return


@router.get("/{id}")
async def article_by_id(id: int):
    """
    根据id获取某一文章的全部信息
    :param id: 文章的id
    :return: 文章的完整信息Json
            ```
            {
                "article_id": 文章id,
                "article_name": 文章标题,
                "article_series": 文章所属系列的id，可能为空,
                "update_time": 文章更新日期,
                "article_cover": 文章封面的URL,
                "article_abstract": 文章摘要（Markdown）,
                "article_content": 文章正文（Markdown）,
                "article_category": 文章所属category的id
            }
            ```
    """
    pass

@router.get("/categories")
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

@router.get("/series/{series_id}")
async def series_by_id(series_id: int):
    """
    TODO: 未来实现，通过series_id查询系列
    :param series_id:
    :return: TODO: 未来实现，文章系列的信息
    """
    pass