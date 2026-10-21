# rpa-robot

![tests](https://github.com/Arutggg/rpa-robot/actions/workflows/tests.yml/badge.svg)

Веб-сервис на FastAPI, который запускает и останавливает робота. Робот это отдельный Python-скрипт: каждую секунду печатает в консоль следующее число, начиная с заданного.

## Требования

Python 3.10+

## Установка и запуск

Windows:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app
```

Документация API и запросы из браузера: http://127.0.0.1:8000/docs

На Windows робот открывается в отдельном окне консоли. На macOS и Linux его вывод идёт в терминал, где запущен сервис.

Робота можно запустить и без сервиса:

```
python robot/robot.py --start 10
```

## API

| Метод | Путь | Описание |
|---|---|---|
| POST | `/robot/start` | Запустить робота. Тело необязательное: `{"start_number": 10}`, по умолчанию 0 |
| POST | `/robot/stop` | Остановить робота |
| GET | `/robot/status` | Статус: запущен ли, pid, с какого числа, время старта |
| GET | `/robot/runs` | История запусков: время старта и окончания, длительность, начальное число |

Повторный запуск работающего робота и остановка незапущенного возвращают 409.

## Как устроено

- `robot/robot.py`: сам робот, асинхронный счётчик на asyncio. Про API ничего не знает.
- `app/robot_manager.py`: запускает робота отдельным процессом через `subprocess.Popen` и останавливает его. Отдельный поток ждёт завершения процесса и записывает в базу время окончания, поэтому запуск фиксируется, даже если робот упал или окно консоли закрыли вручную.
- `app/db.py`: SQLite через стандартный `sqlite3`. Файл `robot.db` создаётся в корне проекта при старте сервиса.
- `app/main.py`: эндпоинты. При остановке сервиса робот тоже останавливается.

## Тесты

```
pip install -r requirements-dev.txt
pytest
```

Тесты запускаются в GitHub Actions на Windows, Ubuntu и macOS.