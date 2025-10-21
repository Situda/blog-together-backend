import tomlkit
from sqlalchemy import URL


def get_database_url():
    with open("../config.toml", encoding='utf-8') as f:
        config: dict = tomlkit.parse(f.read())


    database_config: dict = config['database']
    if database_config['type'] == 'sqlite':
        database_url: str | URL = f"sqlite+aiosqlite:///../{database_config['name']}.db"
    else:
        if database_config['type'] == 'mysql':
            database_config['type'] += '+asyncmy'
        else:
            raise Exception(f"Unknown database type: {database_config['type']}. Please use `sqlite` or `mysql`.")
        # TODO: 未来需要处理本地不存在指定名称的数据库的情况
        database_url: str | URL = URL.create(
            database_config['type'],
            username=database_config['username'],
            password=database_config['password'],
            host=database_config['host'],
            port=database_config['port'] if len(database_config['port']) > 0 else None,
            database=database_config['name']
        )
        # engine = create_engine(database_url)
        #
        # try:
        #     with engine.connect() as connection:
        #         create_database: str = f'CREATE DATABASE IF NOT EXISTS {database_config["name"]}'
        #         connection.execute(text(create_database))
        #         connection.commit()
        # except Exception as e:
        #     print(e)
        # finally:
        #     engine.dispose()
        #
        # database_url = database_url.set(database=database_config['name'])
    return database_url
