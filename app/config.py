import tomlkit
import os
from sqlalchemy import URL, create_engine, text


def get_database_url():
    with open("../config.toml", encoding='utf-8') as f:
        config: dict = tomlkit.parse(f.read())


    database_config: dict = config['database']
    if database_config['type'] == 'sqlite':
        database_url: str | URL = f"sqlite+aiosqlite:///../{database_config['name']}.db"
    elif database_config['type'] == 'mysql':
        database_url: str | URL = URL.create(
            database_config['type'],
            username=database_config['username'],
            password=database_config['password'],
            host=database_config['host'],
            port=database_config['port'] if len(database_config['port']) > 0 else None,
            # database=database_config['name']
        )
        engine = create_engine(database_url)

        # 若数据库不存在则创建数据库
        try:
            with engine.connect() as connection:
                create_database: str = f'CREATE DATABASE IF NOT EXISTS {database_config["name"]};'
                connection.execute(text(create_database))
                connection.commit()
        except Exception as e:
            print(e)
            exit(-1)
        finally:
            engine.dispose()
        database_config['type'] += '+asyncmy'
        database_url = database_url.set(
            drivername=database_config['type'],
            database=database_config['name']
        )
    else:
        raise Exception(f"Unknown database type: {database_config['type']}. Please use `sqlite` or `mysql`.")
    return database_url
