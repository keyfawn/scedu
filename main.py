import asyncio

from system.db import create_tables
from system.utils import cutie, text
from system.utils.menu import Menu


async def main():
    eng = await create_tables()
    """покдлючения к БД"""

    menu = Menu(eng=eng)
    """работа программы"""

    while True:
        ind = cutie.select(text.button_menu, selected_index=menu.select_index, pre_print=text.start)
        """выбранный пункт главного меню"""

        match ind:
            case 0: await menu.actual_scedu()
            case 1: await menu.set_scedu()
            case 2: await menu.set_teachers()
            case 3: await menu.set_obj3cts()
            case 4: await menu.set_kabinets()
            case 5: await menu.about()
            case 6: await menu.ex1t()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
