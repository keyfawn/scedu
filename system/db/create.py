import os

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from system.db.models import Base_sce_day, Haha, get_day


async def run_obj3ct(engine: AsyncEngine):
    """
    создание таблицы Предметы
    :param engine: подключения к БД
    """
    async with engine.begin() as conn:
        await conn.run_sync(Haha.metadata.create_all)


async def run_teacher(engine: AsyncEngine):
    """
    создание таблицы Преподаватели
    :param engine: подключения к БД
    """
    async with engine.begin() as conn:
        await conn.run_sync(Haha.metadata.create_all)


async def run_kabinet(engine: AsyncEngine):
    """
    создание таблицы Кабинеты
    :param engine: подключения к БД
    """
    async with engine.begin() as conn:
        await conn.run_sync(Haha.metadata.create_all)


async def run_day(day_of_week: str):
    """
    создание таблицы дня недели
    :param day_of_week: день недели
    """
    from system.db import engine_day
    async with engine_day.get_engine().begin() as conn:
        if not await conn.run_sync(lambda sync_conn: inspect(sync_conn).has_table(f'day_{day_of_week}')):
            table = get_day(day_of_week)
            await conn.run_sync(Base_sce_day.metadata.create_all)


class Engine:
    def __init__(self, path):
        """
        хранение подключений к БД
        :param path: путь к БД
        """
        if not os.path.isdir('db_files'):
            os.mkdir('db_files')
        self.engine = create_async_engine(url=path)

    def get_engine(self):
        """
        Возвращение покдлючения
        :return: подключение
        """
        return self.engine


class Engines:
    def __init__(self, day: async_sessionmaker, data: async_sessionmaker):
        """
        хранение подключения к БД
        :param day: БД "дни недели"
        :param data: БД "предметы, преподаватели, кабинеты"
        """
        self.day: async_sessionmaker = day()
        self.data: async_sessionmaker = data()


class SessionMiddleware:
    def __init__(self, day: AsyncSession, data: AsyncSession):
        """
        подключения к БД
        :param day: БД "дни недели"
        :param data: БД "предметы, преподаватели, кабинеты"
        """
        self.day: AsyncSession = day
        self.data: AsyncSession = data
