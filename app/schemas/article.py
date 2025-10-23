from pydantic import BaseModel

class Items(BaseModel):
    """
    :param category: 文章category，可选，默认"all"，表示查询所有文章
    :param is_series: 系列文章过滤器，True表示只返回系列文章的入口信息，False表示返回单个文章和系列文章的信息，默认False
    :param page: 文章分页时的第几页，默认1
    :param limit: 每页的返回文章信息数量，默认9
    """
    category: str = "all"
    is_series: bool = False
    page: int = 1
    limit: int = 9