import tomlkit
from sqlalchemy import create_engine, Column, Unicode, Integer, String, UnicodeText

from app.models.base import Base


class Projects(Base):
    """
    项目表
    """
    __tablename__ = 'projects'
    project_id: Integer = Column('project_id', Integer, primary_key=True)
    project_name: Unicode = Column('project_name', Unicode(30), nullable=False)
    project_description: Unicode = Column('project_description', UnicodeText, nullable=False)
    project_cover: String = Column('project_cover', String(1024), nullable=False)


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

