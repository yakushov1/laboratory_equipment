# database.py - функции для работы с БД
import pymysql
from pymysql.cursors import DictCursor
import config

def get_connection():
    """Создает подключение к БД"""
    return pymysql.connect(
        host=config.DB_CONFIG['host'],
        user=config.DB_CONFIG['user'],
        password=config.DB_CONFIG['password'],
        database=config.DB_CONFIG['database'],
        charset=config.DB_CONFIG['charset'],
        cursorclass=DictCursor
    )

def execute_query(query, params=None, fetchall=True, commit=False):
    """
    Универсальная функция для выполнения SQL запросов
    
    Args:
        query: SQL запрос
        params: параметры для запроса
        fetchall: True - вернуть все строки, False - вернуть одну строку
        commit: True - сделать commit после выполнения
    Returns:
        Результат запроса или None
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if commit:
                conn.commit()
                return cursor.lastrowid  # Возвращает ID новой записи
            
            if fetchall:
                return cursor.fetchall()
            else:
                return cursor.fetchone()
    except Exception as e:
        if commit:
            conn.rollback()
        raise e
    finally:
        conn.close()

def execute_non_query(query, params=None):
    """Специализированная функция для INSERT/UPDATE/DELETE"""
    return execute_query(query, params, fetchall=False, commit=True)

def test_connection():
    """Проверяет подключение к БД"""
    try:
        result = execute_query("SELECT 1 as test")
        print("✅ Подключение к БД успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

###################################################
#           СТАТИСТИКА ДЛЯ ГЛАВНОЙ СТРАНИЦЫ
###################################################

def get_equipment_amount():
    """Возвращает суммарное количество оборудования по категориям"""
    query = """
        SELECT equipmentCategory.title, COUNT(*) AS amount
        FROM equipment
        LEFT JOIN equipmentCategory ON equipment.categoryId = equipmentCategory.id
        GROUP BY equipmentCategory.title
        ORDER BY amount DESC
    """
    return execute_query(query)

def get_staff_amount():
    """Возвращает количество сотрудников по ролям"""
    query = """
        SELECT roles.title, COUNT(*) as amount
        FROM staff LEFT JOIN roles ON staff.roleId = roles.id
        GROUP BY roles.title
    """
    return execute_query(query)

def get_maintenance_planned():
    """Возвращает список запланированного ремонта"""
    query = """
        SELECT eM.id, eM.maintenanceDate, e.serialNo, e.title, s.surname, r.title AS role
        FROM equipmentMaintenance eM 
        LEFT JOIN equipment e ON eM.equipmentId = e.id
        LEFT JOIN maintenanceStatus mS ON eM.statusId = mS.id
        LEFT JOIN staff s ON eM.staffId = s.id
        LEFT JOIN roles r ON s.roleId = r.id
        WHERE mS.title = 'запланировано'
        ORDER BY eM.maintenanceDate
    """
    return execute_query(query)

##############################################################
#           ЗАПРОСЫ ДЛЯ СТРАНИЦЫ ОБОРУДОВАНИЕ
##############################################################

def get_all_equipment():
    """Получить всё оборудование с названиями категорий и статусов"""
    query = """
        SELECT e.*, ec.title as category, es.title as status 
        FROM equipment e
        LEFT JOIN equipmentCategory ec ON e.categoryId = ec.id
        LEFT JOIN equipmentStatus es ON e.statusId = es.id
        ORDER BY e.id
    """
    return execute_query(query)

def get_all_categories():
    """Получить все категории оборудования"""
    return execute_query("SELECT * FROM equipmentCategory ORDER BY title")

def get_all_statuses():
    """Получить все статусы оборудования"""
    return execute_query("SELECT * FROM equipmentStatus ORDER BY title")

def add_equipment(title, serialNo, categoryId, statusId):
    """Добавить новое оборудование"""
    query = """
        INSERT INTO equipment (title, serialNo, categoryId, statusId) 
        VALUES (%s, %s, %s, %s)
    """
    return execute_non_query(query, (title, serialNo, categoryId, statusId))

def update_equipment(id, title, serialNo, categoryId, statusId):
    """Обновить существующее оборудование"""
    query = """
        UPDATE equipment 
        SET title = %s, serialNo = %s, categoryId = %s, statusId = %s
        WHERE id = %s
    """
    return execute_non_query(query, (title, serialNo, categoryId, statusId, id))

def delete_equipment(id):
    """Удалить оборудование"""
    return execute_non_query("DELETE FROM equipment WHERE id = %s", (id,))

##############################################################
#           ЗАПРОСЫ ДЛЯ СТРАНИЦЫ СОТРУДНИКИ
##############################################################

def get_all_staff():
    """Выводит список всех сотрудников с roleId"""
    query = """
        SELECT s.id, r.title, s.surname, s.name, s.roleId
        FROM staff s LEFT JOIN roles r ON s.roleId = r.id
    """
    return execute_query(query)

def get_all_staff_roles():
    """Выводит список всех ролей (должностей) сотрудников"""
    return execute_query("SELECT * FROM roles ORDER BY title")

def add_staff(surname, name, roleId):
    """Добавить нового сотрудника"""
    query = """
        INSERT INTO staff (surname, name, roleId) 
        VALUES (%s, %s, %s)
    """
    return execute_non_query(query, (surname, name, roleId))

def update_staff(id, surname, name, roleId):
    """Обновить существующего сотрудника"""
    query = """
        UPDATE staff 
        SET surname = %s, name = %s, roleId = %s
        WHERE id = %s
    """
    return execute_non_query(query, (surname, name, roleId, id))

def delete_staff(id):
    """Удалить сотрудника"""
    return execute_non_query("DELETE FROM staff WHERE id = %s", (id,))

##############################################################
#           ЗАПРОСЫ ДЛЯ СТРАНИЦЫ ОБСЛУЖИВАНИЕ
##############################################################

def get_all_maintenance():
    """Получить все записи обслуживания с дополнительной информацией"""
    query = """
        SELECT 
            em.id,
            em.maintenanceDate,
            em.equipmentId,
            em.statusId,
            em.staffId,
            e.title as equipment_title,
            e.serialNo,
            ms.title as status_title,
            s.surname,
            s.name
        FROM equipmentMaintenance em
        LEFT JOIN equipment e ON em.equipmentId = e.id
        LEFT JOIN maintenanceStatus ms ON em.statusId = ms.id
        LEFT JOIN staff s ON em.staffId = s.id
        ORDER BY em.maintenanceDate DESC
    """
    return execute_query(query)

def get_all_maintenance_statuses():
    """Получить все статусы обслуживания"""
    return execute_query("SELECT * FROM maintenanceStatus ORDER BY title")

def add_maintenance(maintenanceDate, equipmentId, statusId, staffId):
    """Добавить запись обслуживания"""
    query = """
        INSERT INTO equipmentMaintenance 
        (maintenanceDate, equipmentId, statusId, staffId)
        VALUES (%s, %s, %s, %s)
    """
    return execute_non_query(query, (maintenanceDate, equipmentId, statusId, staffId))

def update_maintenance(id, maintenanceDate, equipmentId, statusId, staffId):
    """Обновить запись обслуживания"""
    query = """
        UPDATE equipmentMaintenance 
        SET maintenanceDate = %s, 
            equipmentId = %s, 
            statusId = %s, 
            staffId = %s
        WHERE id = %s
    """
    return execute_non_query(query, (maintenanceDate, equipmentId, statusId, staffId, id))

def delete_maintenance(id):
    """Удалить запись обслуживания"""
    return execute_non_query("DELETE FROM equipmentMaintenance WHERE id = %s", (id,))

##############################################################
#           ЗАПРОСЫ ДЛЯ СТРАНИЦЫ ЗАКУПКИ
##############################################################

def get_all_purchases():
    """Все закупки с equipmentId для редактирования"""
    query = """
        SELECT p.*, e.title as equipment_title, ps.title as status_title
        FROM purchase p
        LEFT JOIN equipment e ON p.equipmentId = e.id
        LEFT JOIN purchaseStatus ps ON p.statusId = ps.id
        ORDER BY p.purchaseDate DESC
    """
    return execute_query(query)

def get_all_purchase_statuses():
    """Все статусы закупок"""
    return execute_query("SELECT * FROM purchaseStatus ORDER BY title")

def add_purchase(purchaseDate, equipmentId, quantity, cost, statusId):
    """Добавить закупку"""
    query = """
        INSERT INTO purchase (purchaseDate, equipmentId, quantity, cost, statusId)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_non_query(query, (purchaseDate, equipmentId, quantity, cost, statusId))

def update_purchase(id, purchaseDate, equipmentId, quantity, cost, statusId):
    """Обновить закупку"""
    query = """
        UPDATE purchase 
        SET purchaseDate = %s, equipmentId = %s, 
            quantity = %s, cost = %s, statusId = %s
        WHERE id = %s
    """
    return execute_non_query(query, (purchaseDate, equipmentId, quantity, cost, statusId, id))

def delete_purchase(id):
    """Удалить закупку"""
    return execute_non_query("DELETE FROM purchase WHERE id = %s", (id,))

##############################################################
#           ДОПОЛНИТЕЛЬНЫЕ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
##############################################################

def get_equipment_by_id(id):
    """Получить оборудование по ID (для редактирования)"""
    query = "SELECT * FROM equipment WHERE id = %s"
    return execute_query(query, (id,), fetchall=False)

def get_staff_by_id(id):
    """Получить сотрудника по ID (для редактирования)"""
    query = "SELECT * FROM staff WHERE id = %s"
    return execute_query(query, (id,), fetchall=False)

def search_equipment_by_serial(serial_no):
    """Поиск оборудования по серийному номеру"""
    query = "SELECT * FROM equipment WHERE serialNo LIKE %s"
    return execute_query(query, (f"%{serial_no}%",))

def get_pending_maintenance():
    """Получить просроченное обслуживание"""
    query = """
        SELECT * FROM equipmentMaintenance 
        WHERE maintenanceDate < CURDATE() 
        AND statusId IN (SELECT id FROM maintenanceStatus WHERE title = 'запланировано')
    """
    return execute_query(query)