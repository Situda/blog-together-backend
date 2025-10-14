import tomlkit
from sqlalchemy import create_engine, Column, Unicode, Integer, DateTime, String, UnicodeText
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Articles(Base):
    """
    文章表
    """
    __tablename__ = 'articles'

    article_id: Integer = Column('article_id', Integer, primary_key=True)
    article_name: Unicode = Column('article_name', Unicode(30), nullable=False)  # 最长存储30个unicode字符长度的文本
    article_series: Integer = Column('article_series', Integer, nullable=True)  # 所属于的系列id
    update_time: DateTime = Column('update_time', DateTime, nullable=False)
    article_cover: String = Column('article_cover', String(1024), nullable=False)  # 文章封面的URL
    article_abstract: String = Column('article_abstract', UnicodeText, nullable=False)   # 文章摘要（Markdown）
    article_content: UnicodeText = Column('article_content', UnicodeText, nullable=False)   # 文章正文（Markdown）
    article_tag: Integer = Column('article_tag', Integer, nullable=False)   # 文章类型id

    def __repr__(self):
        return (f'Articles(article_id={self.article_id}, article_name={self.article_name}, '
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

class Projects(Base):
    """
    项目表
    """
    __tablename__ = 'projects'
    project_id: Integer = Column('project_id', Integer, primary_key=True)
    project_name: Unicode = Column('project_name', Unicode(30), nullable=False)
    project_description: Unicode = Column('project_description', UnicodeText, nullable=False)
    project_cover: String = Column('project_cover', String(1024), nullable=False)

class ArticleTags(Base):
    """
    文章类型表
    """
    __tablename__ = 'article_tags'
    article_tag_id: Integer = Column('article_tag_id', Integer, primary_key=True)
    article_tag_name: Unicode = Column('article_tag_name', Unicode(30), nullable=False)

    def __repr__(self):
        return f'ArticleTypes(article_tag_id={self.article_tag_id}, article_tag_name={self.article_tag_name})'


with open("../config.toml", encoding='utf-8') as f:
    config: dict = tomlkit.parse(f.read())


database_config: dict = config['database']
if database_config['type'] == 'sqlite':
    database_url = f"sqlite:///../{database_config['name']}.db"
else:
    database_url = (f"{database_config['type']}://"
                    f"{database_config['username']}:{database_config['password']}"
                    f"@{database_config['server']}/{database_config['name']}")

engine = create_engine(database_url)

Base.metadata.create_all(engine)

