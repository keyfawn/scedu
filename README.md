<h1 align="center">Scedu</h1>
<p align="center">

<img src="https://img.shields.io/github/languages/top/keyfawn/scedu">
<img src="https://img.shields.io/github/license/keyfawn/scedu">
<img src="https://img.shields.io/github/v/release/keyfawn/scedu">
<img src="https://img.shields.io/github/watchers/keyfawn/scedu">
<br>
<img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
<img src="https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white">
<img src="https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white">
<a href="https://l3ssol3g.t.me/"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>

</p>

_Управления расписанием учебного заведения_

---

Приложение «Расписание для учебного заведения» предназначено для автоматизации процесса составления расписания занятий. Оно позволяет удобно управлять учебным процессом, учитывая все особенности учебного заведения.

## Посмотреть демо
![text](https://i.imgur.com/8m1vD2G.gif)

## Технологии в проекте
**SQLAlchemy** - асинхронная работа с БД

**aiosqlite** - вид БД

**cutie** - реализация главного меню посредством клавиш вверх-вниз _(модифицированный)_

## Структура программы
- **main.py** - главный и запускаемый файл
- **requirements.txt** - файл с необходимыми библиотеками
- **system**
  - **db**
    - **__init__.py** - создание таблиц БД
    - **create.py** - отдельные функции создание каждой таблицы
  - **utils**
    - **cutie.py** - модифицированный cutie для меню
    - **menu.py** - главная работа меню
    - **text.py** - файл с текстом для программы
- **LICENCE** - файл лицензии
- **run.bat** - файл установки необходимого софта для Windows

## Как запустить?
### Windows
Варианты:
- Скачать готовый [exe](https://github.com/keyfawn/Scedu/releases/) и запустить
- Запустить *run.bat*, затем только *main.py*
- Вариант как для [Linux](#linux)

### Linux
Установить Python 3.12

Для запуска необходимо с помощью файла *requirements.txt* установить все нужные библиотеки:
    
```pip install -r requirements.txt```

После запустить *main.py*, и программа будет запущена

## Контакты
[Мой тг](https://l3ssol3g.t.me/)

[Моя зеленка](https://lolz.live/l3ssol3g/)

## Предыдущая работа по тз

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=keyfawn&repo=bookery)](https://github.com/keyfawn/bookery)
