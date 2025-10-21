from sqlalchemy import Column, Unicode, Integer, String, UnicodeText
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.config import get_database_url

class Projects(Base):
    """
    项目表
    """
    __tablename__ = 'projects'
    project_id: Integer = Column('project_id', Integer, primary_key=True)
    project_name: Unicode = Column('project_name', Unicode(30), nullable=False)
    project_description: Unicode = Column('project_description', UnicodeText, nullable=False)
    project_cover: String = Column('project_cover', String(1024), nullable=False)


database_url = get_database_url()
# engine = create_engine(database_url)
async_engine = create_async_engine(database_url)

# Base.metadata.create_all(engine)

async def create_db():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

