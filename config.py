# config.py - настройки подключения к БД
# ниже приведены тестовые настройки - НЕ ЯВЛЯЮТСЯ РАБОЧИМИ

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           
    'password': '123456789',  
    'database': 'lab_equipment',
    'charset': 'utf8mb4',
    'cursorclass': 'DictCursor'  # чтобы результаты были словарями
}

