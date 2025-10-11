import tomlkit
from sqlalchemy import create_engine

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
engine.connect()
engine.dispose()