from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base_sce_day = declarative_base()
Haha = declarative_base()


class Day(Base_sce_day):
    """таблица "День недели" """

    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    """id"""

    obj3ct_id = Column(Integer)
    """id предмета"""

    kabinet_id = Column(Integer)
    """id кабинета"""

    teacher_id = Column(Integer)
    """id преподавателя"""

    hide = Column(Boolean, default=True)
    """удалён или нет"""


def get_day(day_of_week):
    """
    получение таблицы день недели
    :param day_of_week: день недели
    :return: таблица
    """
    tablename = 'day_%s' % day_of_week  # dynamic table name
    class_name = 'table_%s' % day_of_week  # dynamic class name
    Model = type(class_name, (Day,), {'__tablename__': tablename})
    return Model


assoc_tea_obj = Table("assoc_tea_obj", Haha.metadata,
                      Column("teacher_id", Integer, ForeignKey("teachers.id")),
                      Column("obj3ct_id", Integer, ForeignKey("obj3cts.id")))
"""помогающая таблица для модели отношений Многие ко многим (преподаватели - предметы)"""


assoc_kab_obj = Table("assoc_kab_obj", Haha.metadata,
                      Column("kabinet_id", Integer, ForeignKey("kabinets.id")),
                      Column("obj3ct_id", Integer, ForeignKey("obj3cts.id")))
"""помогающая таблица для модели отношений Многие ко многим (кабинеты - предметы)"""


class Teacher(Haha):
    """таблица Преподаватель"""

    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """id преподавателя"""

    surname = Column(String)
    """фамилия преподавателя"""

    name = Column(String)
    """имя преподавателя"""

    patronymic = Column(String)
    """отчество преподавателя"""

    obj3cts_id = relationship("Obj3ct", secondary=assoc_tea_obj, back_populates="teachers_id")
    """отношение к объекту Предмет"""

    hide = Column(Boolean, default=True)
    """удалён или нет"""


class Kabinet(Haha):
    """таблица Кабинет"""

    __tablename__ = "kabinets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """id кабинета"""

    count = Column(Integer)
    """номер кабинета"""

    max_students = Column(Integer)
    """максимальное количество студентов в кабинете"""

    obj3cts_id = relationship("Obj3ct", secondary=assoc_kab_obj, back_populates="kabinets_id")
    """отношение к объекту Предмет"""

    hide = Column(Boolean, default=True)
    """удалён или нет"""


class Obj3ct(Haha):
    """таблица Предмет"""

    __tablename__ = "obj3cts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """id предмета"""

    title = Column(String)
    """название предмета"""

    teachers_id = relationship("Teacher", secondary=assoc_tea_obj, back_populates="obj3cts_id")
    """отношения к объектам Преподаватели"""

    kabinets_id = relationship("Kabinet", secondary=assoc_kab_obj, back_populates="obj3cts_id")
    """отношения к объектам Кабинеты"""

    hide = Column(Boolean, default=True)
    """удалён или нет"""
