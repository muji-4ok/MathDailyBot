### Math Daily

This is a Telegram bot with a base of math problems with three different topics and a difficulty setting from 0 to 4 (very easy to insane).
You ask the bot to send a problem by clicking the **"Give task"** button. 

The possible commands are:
1. Send a problem. Before receiving a task there is an option to choose the area (Set theory, Geometry, Logic and Combinatorics)
1. Give a hint (there is one hint for each problem)
2. Give a solution

It is made sure that you don't get the same probem twice.

## Startup

Нужно сделать вот это:

1. Создать файл `src/keys.py` и в нем создать переменную `TG_BOT_TOKEN='<YOUR TELEGRAM BOT TOKEN>'`
2. Запустить `docker compose up`
3. Экспортировать базу с задачами в CSV и положить в `data/tasks.csv`
4. Запустить `scripts/create_db.sh`
