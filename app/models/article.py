from sqlalchemy import Integer, Column, Unicode, DateTime, String, UnicodeText

from app.models.base import Base


class Articles(Base):
    """
    文章表
    """
    __tablename__ = 'articles'

    article_id: Integer = Column('article_id', Integer, primary_key=True)
    article_title: Unicode = Column('article_title', Unicode(30), nullable=False)  # 最长存储30个unicode字符长度的文本
    article_series: Integer = Column('article_series', Integer, nullable=True)  # 所属于的系列id
    update_time: DateTime = Column('update_time', DateTime, nullable=False)
    article_cover: String = Column('article_cover', String(1024), nullable=False)  # 文章封面的URL
    article_abstract: String = Column('article_abstract', UnicodeText, nullable=False)   # 文章摘要（Markdown）
    article_content: UnicodeText = Column('article_content', UnicodeText, nullable=False)   # 文章正文（Markdown）
    article_category: Integer = Column('article_category', Integer, nullable=False)   # 文章类型id

    def __repr__(self):
        return (f'Articles(article_id={self.article_id}, article_title={self.article_title}, '
                f'article_series={self.article_series}, update_time={self.update_time})')


class ArticleSeries(Base):
    """
    文章集表
    """
    __tablename__ = 'article_series'

    series_id: Integer = Column('series_id', Integer, primary_key=True)
    series_name: Unicode = Column('series_name', Unicode(30), nullable=False)
    series_description: Unicode = Column('series_description', UnicodeText, nullable=False)
    series_cover: String = Column('series_cover', String(1024), nullable=False)


class ArticleCategories(Base):
    """
    文章category表
    """
    __tablename__ = 'article_categories'
    article_category_id: Integer = Column('article_category_id', Integer, primary_key=True)
    article_category_name: Unicode = Column('article_category_name', Unicode(30), nullable=False, unique=True)

    def __repr__(self):
        return f'ArticleCategories(article_category_id={self.article_category_id}, article_category_name={self.article_category_name})'
