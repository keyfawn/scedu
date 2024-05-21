from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from system.db import SessionMiddleware, get_day, Teacher, Kabinet, Obj3ct
from system.utils import cutie, text


class Menu:
    def __init__(self, eng: SessionMiddleware):
        """
        класс с основной работой программы
        :param eng: подключения к БД
        """
        self.eng = eng
        """подлючения к бд"""

        self.select_index = 0
        """выбранный пункт"""

    async def actual_scedu(self):
        """Расписание на сегодня"""
        week = {0: "pn", 1: "vt", 2: "sr", 3: "cht", 4: "pt", 5: "sb", 6: "vs"}
        day_of_week = week[datetime.now().weekday()]
        """сегодняшний день недели"""

        table = get_day(day_of_week)
        """таблица с текущим днём"""

        obj3cts = (await self.eng.day.execute(select(table).where(table.hide == 1))).scalars().fetchall()
        """предметы на текущий день"""

        ac_pre = []
        """список с информацией об предметах"""
        for _ in obj3cts:
            ob3 = (await self.eng.data.execute(select(Obj3ct).where(Obj3ct.id == _.obj3ct_id,
                                                                    Obj3ct.hide == 1))).scalar_one_or_none()
            te3 = ((await self.eng.data.execute(select(Teacher).where(Teacher.id == _.teacher_id,
                                                                      Teacher.hide == 1))).scalar_one_or_none())
            ka3 = ((await self.eng.data.execute(select(Kabinet).where(Kabinet.id == _.kabinet_id,
                                                                      Kabinet.hide == 1))).scalar_one_or_none())
            ac_pre.append(text.exanple_actual_predmet.format(ob3.title if ob3 else "none",
                                                             ka3.count, ka3.max_students,
                                                             te3.surname if te3 else "none",
                                                             te3.name if te3 else "none",
                                                             te3.patronymic if te3 else "none"))

        self.select_index = 0
        cutie.select(['Назад'], pre_print='\n'.join(ac_pre) if ac_pre else text.no_actual_objects)

    async def set_scedu(self):
        """Изменить расписание"""
        self.select_index = 0
        async with self.eng.day as sessy_day:
            async with self.eng.data as sessy_data:

                while True:
                    day_of_week = cutie.select(['Понедельник', 'Вторник', "Среда", "Четверг", "Пятница",
                                                "Суббота", "Воскресенье", '', 'Назад'], caption_indices=[7],
                                               selected_index=self.select_index, pre_print=text.set_day_of_week)
                    """выбранный день недели"""

                    #  если выбран Назад
                    if day_of_week > 6:
                        break

                    days = {0: 'pn', 1: 'vt', 2: 'sr', 3: 'cht', 4: 'pt', 5: 'sb', 6: 'vs'}
                    day = days[day_of_week]
                    table = get_day(day)
                    """таблица с выбранным днём"""

                    self.select_index = 0

                    while True:
                        predmets = (await sessy_day.execute(select(table).where(table.hide == 1))).scalars().fetchall()
                        """предметы в выбранный день"""

                        prep = {}
                        """словарь с данными о предметах"""

                        for ind, pre in enumerate(predmets):
                            id_predmet = pre.id
                            obj3ct = ((await sessy_data.execute(select(Obj3ct).where(
                                Obj3ct.id == pre.obj3ct_id, Obj3ct.hide == 1))).scalar_one_or_none())
                            kabinet = ((await sessy_data.execute(select(Kabinet).where(
                                Kabinet.id == pre.kabinet_id, Kabinet.hide == 1))).scalar_one_or_none())
                            teacher = ((await sessy_data.execute(select(Teacher).where(
                                Teacher.id == pre.teacher_id, Teacher.hide == 1))).scalar_one_or_none())
                            prep[ind] = [obj3ct, teacher, kabinet, id_predmet]

                        ind = cutie.select([*[f'{_[0].title if _[0] else "none"}'
                                              for _ in prep.values()], 'Добавить новый', 'Назад'],
                                           pre_print=text.vot_day,
                                           selected_index=self.select_index)

                        #  информация о предмете
                        if ind < len(predmets):
                            await self._info_day_predmet(prep=prep, ind=ind, sessy_day=sessy_day, table=table)

                        #  добавить новый предмет
                        elif ind == len(predmets):
                            await self._new_day_predmet(sessy_data=sessy_data, table=table, predmets=predmets)

                        #  если Назад
                        else:
                            self.select_index = day_of_week
                            break
        self.select_index = 1

    async def _info_day_predmet(self, prep, ind, sessy_day, table):
        """информация о выбранном предмете"""
        sel_pre = prep[ind]
        sel_pre_obj = (await sessy_day.execute(select(table).where(table.id == sel_pre[3], table.hide == 1
                                                                   ))).scalar_one()
        """выбранный предмет"""

        while True:
            self.select_index = ind
            t34 = text.example_predmet.format(sel_pre[0].title if sel_pre[0] else "none",
                                              sel_pre[1].surname if sel_pre[1] else "none",
                                              sel_pre[1].name if sel_pre[1] else "none",
                                              sel_pre[1].patronymic if sel_pre[1] else "none",
                                              sel_pre[2].count if sel_pre[2] else "none",
                                              sel_pre[2].max_students if sel_pre[2] else "none")
            inde = cutie.select(['Удалить', 'Назад'], pre_print=t34)
            match inde:
                #  удаление предмета
                case 0:
                    if cutie.prompt_yes_or_no(text.delete_predmet, yes_text='Да', no_text='Нет'):
                        sel_pre_obj.hide = False
                        await self.eng.day.commit()
                        cutie.select(['Назад'], pre_print=text.delete_predmet_good)
                        break
                #  назад
                case 1:
                    break

    async def _new_day_predmet(self, sessy_data, table, predmets):
        while True:
            obj3cts = (await sessy_data.execute(select(Obj3ct).where(Obj3ct.hide == 1).
                                                options(selectinload(Obj3ct.teachers_id),
                                                        selectinload(Obj3ct.kabinets_id)))).scalars().fetchall()
            """все предметы"""

            obj3 = {ind: obj for ind, obj in enumerate(obj3cts)}
            """словарь с предметами"""

            ind_obj = cutie.select([*[_.title for _ in obj3.values()], 'Назад'], pre_print=text.set_obj3ct)
            """выбранный предмет индекс"""

            #  если Назад
            if ind_obj >= len(obj3cts):
                break

            select_obj3ct = obj3[ind_obj]
            """выбранный предмет"""

            is_pri = True
            """проверка на условие: препод не больше 5 предметов в день"""

            while True:
                tea3 = {ind: tit for ind, tit in enumerate(select_obj3ct.teachers_id)}
                """словарь с преподавателя"""

                ind_tea = cutie.select([*[f'{_.surname} {_.name} {_.patronymic}'
                                          for _ in select_obj3ct.teachers_id], 'Назад'],
                                       pre_print=text.set_teacher, is_print_logo=is_pri)
                """выбранный преподаватель индекс"""

                #  если Назад
                if ind_tea >= len(select_obj3ct.teachers_id):
                    break

                select_teacher = tea3[ind_tea]
                """выбранный преподаватель"""

                #  проверка на условие: препод не больше 5 предметов в день
                if len((await self.eng.day.execute(select(table).where(table.teacher_id == select_teacher.id,
                                                                       table.hide == 1))).scalars().fetchall()) > 4:
                    cutie.print_logo()
                    print(text.set_teacher_5)
                    is_pri = False
                    continue

                kab3 = {ind: tit for ind, tit in enumerate(select_obj3ct.kabinets_id)}
                """словарь кабинетов"""

                ind_kab = cutie.select([*[f'{_.count}' for _ in select_obj3ct.kabinets_id], 'Назад'],
                                       pre_print=text.set_kabinet)
                """выбранный кабинет индекс"""

                #  если Назад
                if ind_kab >= len(select_obj3ct.kabinets_id):
                    break

                select_kabinet = kab3[ind_kab]
                """выбранный кабинет"""

                #  добавление предмета в выбранный день
                await self.eng.day.merge(table(obj3ct_id=select_obj3ct.id, kabinet_id=select_kabinet.id,
                                               teacher_id=select_teacher.id))
                await self.eng.day.commit()

                cutie.select(['OK'], pre_print=text.set_predmet_good)
                break
            break
        self.select_index = len(predmets)

    async def set_teachers(self):
        """Преподаватели"""
        self.select_index = 0
        while True:
            teachers = (await self.eng.data.execute(select(Teacher).where(Teacher.hide == 1))).scalars().fetchall()
            """все преподаватели"""

            tea = {ind: tit for ind, tit in enumerate(teachers)}
            """словаь с преподавателями"""

            ind = cutie.select([*[f'{_.surname} {_.name} {_.patronymic}'
                                  for _ in tea.values()], 'Добавить нового', 'Назад'], pre_print=text.vot_teachers,
                               selected_index=self.select_index)
            """выбранный преподаватель индекс"""

            #  если выбрал преподавателя
            if ind < len(teachers):
                while True:
                    self.select_index = ind
                    t34 = text.teacher.format(teachers[ind].surname, teachers[ind].name, teachers[ind].patronymic)
                    inde = cutie.select(['Удалить', 'Назад'], pre_print=t34)
                    match inde:
                        #  удаление преподавателя
                        case 0:
                            if cutie.prompt_yes_or_no(text.delete_teacher, yes_text='Да', no_text='Нет'):
                                teachers[ind].hide = False
                                await self.eng.data.commit()
                                cutie.select(['Назад'], pre_print=text.delete_teacher_good)
                                break
                        #  если Назад
                        case 1:
                            break

            #  добавление нового преподавателя
            elif ind == len(teachers):
                while True:
                    cutie.print_logo()
                    inp5t = input(text.new_teacher)

                    #  если Назад
                    if inp5t == 'Назад':
                        break

                    #  если не по правилам
                    #  пример: Иванов Иван Иванович
                    if len(inp5t.split(' ')) != 3:
                        continue

                    surname, name, patronymic = inp5t.split(' ')

                    #  добавление нового преподавателя
                    await self.eng.data.merge(Teacher(surname=surname, name=name, patronymic=patronymic))
                    await self.eng.data.commit()
                    cutie.select(['ОК'], pre_print=text.new_teacher_good)
                    break
                self.select_index = len(teachers)
            else:
                break
        self.select_index = 2

    async def set_obj3cts(self):
        """Уроки"""
        self.select_index = 0
        async with (self.eng.data as sessy):
            while True:
                obj3cts = (await sessy.execute(select(Obj3ct).options(
                    selectinload(Obj3ct.teachers_id), selectinload(Obj3ct.kabinets_id)).
                                               where(Obj3ct.hide == 1))).scalars().fetchall()
                """все предметы"""

                obj3 = {ind: obj for ind, obj in enumerate(obj3cts)}
                """словарь с предметами"""

                ind = cutie.select([*[f'{_.title}' for _ in obj3.values()], 'Добавить новый', 'Назад'],
                                   pre_print=text.vot_obj3cts, selected_index=self.select_index)
                """выбранный предмет индекс"""

                #  если выбран предмет
                if ind < len(obj3cts):
                    while True:
                        self.select_index = ind
                        cutie.print_logo()
                        t34 = text.obj3ct.format(obj3cts[ind].title,
                                                 ', '.join([f'{prepod.surname} {prepod.name} {prepod.patronymic}'
                                                            for prepod in obj3[ind].teachers_id]),
                                                 ', '.join([str(prepod.count)
                                                            for prepod in obj3[ind].kabinets_id]))
                        inde = cutie.select(['Удалить', 'Назад'], pre_print=t34)
                        match inde:
                            #  удаление предмета
                            case 0:
                                if cutie.prompt_yes_or_no(text.delete_obj3ct, yes_text='Да', no_text='Нет'):
                                    obj3cts[ind].hide = False
                                    await sessy.commit()
                                    cutie.select(['Назад'], pre_print=text.delete_obj3ct_good)
                                    break
                            #  если Назад
                            case 1:
                                break

                #  добавление нового предмета
                elif ind == len(obj3cts):
                    while True:
                        cutie.print_logo()
                        title = input(text.new_obj3ct)

                        #  если Назад
                        if title == 'Назад':
                            break

                        teachers = (await sessy.execute(select(Teacher).where(Teacher.hide == 1))).scalars().fetchall()
                        """все преподаватели"""

                        tea = {ind: tit for ind, tit in enumerate(teachers)}
                        """словарь с преподавателями"""

                        l1st_tea = cutie.select_multiple([*[f'{_.surname} {_.name} {_.patronymic}'
                                                            for _ in tea.values()], 'Назад'],
                                                         pre_print=text.vote_teachers, hide_confirm=False)
                        """выбранные преподаватели индексы"""

                        #  если выбраны преподаватели
                        if len(teachers) not in l1st_tea:
                            select_teachers = [tea[ind] for ind in l1st_tea]
                            """выбранные преподаватели"""

                            while True:
                                cutie.print_logo()
                                l1st_kab = input(text.vote_kabinets)

                                #  если Назад
                                if l1st_kab == 'Назад':
                                    break

                                #  если не числа
                                if not all([_.isdigit() for _ in l1st_kab.split(' ')]):
                                    continue

                                select_kabinets = [(await sessy.execute(select(Kabinet).where(
                                    Kabinet.count == int(kab), Kabinet.hide == 1))
                                     ).scalar_one_or_none() for kab in l1st_kab.split(' ')]
                                """выбранные кабинеты"""

                                #  если кабинеты не созданы
                                if not all(select_kabinets):
                                    cutie.select(['Ок'], pre_print=text.not_found_kabinet)
                                    continue

                                #  доавбление предмета
                                obz = Obj3ct(title=title)
                                obz.teachers_id = select_teachers
                                obz.kabinets_id = select_kabinets
                                await sessy.merge(obz)
                                await sessy.commit()
                                cutie.select(['ОК'], pre_print=text.new_obj3ct_good)
                                break

                        #  если Назад
                        break
                    self.select_index = len(obj3cts)

                #  если Назад
                else:
                    break
        self.select_index = 3

    async def set_kabinets(self):
        """Кабинеты"""
        self.select_index = 4
        while True:
            cutie.print_logo()
            count = input(text.search_kabinet)

            #  если Отмена
            if count == 'Отмена':
                break

            #  если не число
            if not count.isdigit():
                continue

            #  если не входит диапазон от 1 по 150
            if int(count) not in range(1, 151):
                continue

            while True:
                cutie.print_logo()
                max_stu = input(text.input_max_students)

                #  если Отмена
                if max_stu == 'Отмена':
                    break

                #  если не число
                if not max_stu.isdigit():
                    continue

                #  добавление кабинета
                await self.eng.data.merge(Kabinet(count=int(count), max_students=int(max_stu)))
                await self.eng.data.commit()
                cutie.select(['ОК'], pre_print=text.kabinet_good)

                break
            break

    async def about(self):
        """Информация"""
        self.select_index = 5
        cutie.select(['Назад'], pre_print=text.about)

    async def ex1t(self):
        """Выход"""
        self.select_index = 6

        #  подтвержение выхода
        if cutie.prompt_yes_or_no(text.pre_exit, yes_text='Да', no_text='Нет'):
            cutie.print_logo()
            print(text.ex1t)
            exit()
