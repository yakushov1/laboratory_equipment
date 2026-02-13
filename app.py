from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'ваш_секретный_ключ'

##############################################################################
# Главная страница
##############################################################################

@app.route('/')
def index():
    """Отображает главную страницу со статистикой"""
    equipment_amount = database.get_equipment_amount()
    staff_amount = database.get_staff_amount()
    maintenance_planned = database.get_maintenance_planned()
    
    return render_template('index.html',
                           equipment_amount=equipment_amount,
                           staff_amount=staff_amount,
                           maintenance_planned=maintenance_planned)


##############################################################################
# Страница сотрудников
##############################################################################

@app.route('/staff')
def staff():
    """Отображает список всех сотрудников"""
    staff_list = database.get_all_staff()
    roles = database.get_all_staff_roles()
    
    return render_template('staff.html', 
                         staff=staff_list,
                         roles=roles)

@app.route('/staff/add', methods=['POST'])
def add_staff():
    """Добавляет нового сотрудника"""
    surname = request.form['surname']
    name = request.form['name']
    roleId = request.form['roleId']
    
    database.add_staff(surname, name, roleId)
    flash('Сотрудник добавлен', 'success')
    return redirect(url_for('staff'))

@app.route('/staff/update/<int:id>', methods=['POST'])
def update_staff(id):
    """Обновляет данные сотрудника"""
    surname = request.form['surname']
    name = request.form['name']
    roleId = request.form['roleId']
    
    database.update_staff(id, surname, name, roleId)
    flash('Изменения сохранены', 'success')
    return redirect(url_for('staff'))

@app.route('/staff/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    """Удаляет сотрудника"""
    database.delete_staff(id)
    flash('Сотрудник удален', 'warning')
    return redirect(url_for('staff'))


##############################################################################
# Страница оборудования
##############################################################################

@app.route('/equipment')
def equipment():
    """Отображает список оборудования"""
    equipment_list = database.get_all_equipment()
    categories = database.get_all_categories()
    statuses = database.get_all_statuses()
    
    return render_template('equipment.html', 
                         equipment=equipment_list,
                         categories=categories,
                         statuses=statuses)

@app.route('/equipment/add', methods=['POST'])
def add_equipment():
    """Добавляет новое оборудование"""
    title = request.form['title']
    serialNo = request.form['serialNo']
    categoryId = request.form['categoryId']
    statusId = request.form['statusId']
    
    database.add_equipment(title, serialNo, categoryId, statusId)
    flash('Оборудование добавлено', 'success')
    return redirect(url_for('equipment'))

@app.route('/equipment/update/<int:id>', methods=['POST'])
def update_equipment(id):
    """Обновляет данные оборудования"""
    title = request.form['title']
    serialNo = request.form['serialNo']
    categoryId = request.form['categoryId']
    statusId = request.form['statusId']
    
    database.update_equipment(id, title, serialNo, categoryId, statusId)
    flash('Изменения сохранены', 'success')
    return redirect(url_for('equipment'))

@app.route('/equipment/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    """Удаляет оборудование"""
    database.delete_equipment(id)
    flash('Оборудование удалено', 'warning')
    return redirect(url_for('equipment'))


##############################################################################
# Страница планового обслуживания
##############################################################################

@app.route('/maintenance')
def maintenance():
    """Отображает график обслуживания оборудования"""
    maintenance_list = database.get_all_maintenance()
    equipment_list = database.get_all_equipment()
    statuses = database.get_all_maintenance_statuses()
    staff_list = database.get_all_staff()
    
    return render_template('maintenance.html',
                         maintenance=maintenance_list,
                         equipment_list=equipment_list,
                         statuses=statuses,
                         staff_list=staff_list)

@app.route('/maintenance/add', methods=['POST'])
def add_maintenance():
    """Добавляет запись о плановом обслуживании"""
    maintenanceDate = request.form['maintenanceDate']
    equipmentId = request.form['equipmentId']
    statusId = request.form['statusId']
    staffId = request.form['staffId']
    
    database.add_maintenance(maintenanceDate, equipmentId, statusId, staffId)
    flash('Обслуживание запланировано', 'success')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/update/<int:id>', methods=['POST'])
def update_maintenance(id):
    """Обновляет запись об обслуживании"""
    maintenanceDate = request.form['maintenanceDate']
    equipmentId = request.form['equipmentId']
    statusId = request.form['statusId']
    staffId = request.form['staffId']
    
    database.update_maintenance(id, maintenanceDate, equipmentId, statusId, staffId)
    flash('Изменения сохранены', 'success')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/delete/<int:id>', methods=['POST'])
def delete_maintenance(id):
    """Удаляет запись об обслуживании"""
    database.delete_maintenance(id)
    flash('Запись удалена', 'warning')
    return redirect(url_for('maintenance'))


##############################################################################
# Страница закупок
##############################################################################

@app.route('/purchases')
def purchases():
    """Отображает список закупок оборудования"""
    purchases_list = database.get_all_purchases()
    equipment_list = database.get_all_equipment()
    statuses = database.get_all_purchase_statuses()
    
    return render_template('purchases.html',
                         purchases=purchases_list,
                         equipment_list=equipment_list,
                         statuses=statuses)

@app.route('/purchases/add', methods=['POST'])
def add_purchase():
    """Добавляет новую закупку"""
    purchaseDate = request.form['purchaseDate']
    equipmentId = request.form.get('equipmentId') or None
    quantity = int(request.form['quantity'])
    cost = float(request.form['cost'])
    statusId = int(request.form['statusId'])
    
    database.add_purchase(purchaseDate, equipmentId, quantity, cost, statusId)
    flash('Закупка добавлена', 'success')
    return redirect(url_for('purchases'))

@app.route('/purchases/update/<int:id>', methods=['POST'])
def update_purchase(id):
    """Обновляет данные о закупке"""
    purchaseDate = request.form['purchaseDate']
    equipmentId = request.form.get('equipmentId') or None
    quantity = int(request.form['quantity'])
    cost = float(request.form['cost'])
    statusId = int(request.form['statusId'])
    
    database.update_purchase(id, purchaseDate, equipmentId, quantity, cost, statusId)
    flash('Изменения сохранены', 'success')
    return redirect(url_for('purchases'))

@app.route('/purchases/delete/<int:id>', methods=['POST'])
def delete_purchase(id):
    """Удаляет запись о закупке"""
    database.delete_purchase(id)
    flash('Закупка удалена', 'warning')
    return redirect(url_for('purchases'))


##############################################################################
# Запуск приложения
##############################################################################

if __name__ == '__main__':
    app.run(debug=True)