from sqlalchemy.ext.asyncio import async_sessionmaker

from system.db import create
from system.db.create import Engine, SessionMiddleware, Engines
from system.db.models import Teacher, get_day, Kabinet, Obj3ct, Base_sce_day, Haha

engine_day = Engine('sqlite+aiosqlite:///db_files/days.db')
"""путь к БД с данными (предметы, преподаватели, кабинеты)"""

engine_data = Engine('sqlite+aiosqlite:///db_files/data.db')
"""пусть к БД с днями"""


async def create_tables() -> SessionMiddleware:
    """
    Создает необходимые таблицы для БД
    :return: готовый класс с подключениями
    """
    session_maker_day = async_sessionmaker(engine_day.get_engine(), expire_on_commit=False)
    session_maker_data = async_sessionmaker(engine_data.get_engine(), expire_on_commit=False)
    eng = Engines(day=session_maker_day, data=session_maker_data)

    await create.run_kabinet(engine_data.get_engine())  # создание таблицы Кабинеты
    await create.run_teacher(engine_data.get_engine())  # создание таблицы Преподаватели
    await create.run_obj3ct(engine_data.get_engine())  # создание таблицы Предметы

    for day in ['pn', 'vt', 'sr', 'cht', 'pt', 'sb', 'vs']:
        await create.run_day(day)  # создание таблицы дней недели

    async with eng.day as session_day:
        async with eng.data as session_data:
            sess = SessionMiddleware(day=session_day, data=session_data)
            """подключения к БД"""

    return sess
