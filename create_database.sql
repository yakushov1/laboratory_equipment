-- роли сотрудников 

CREATE TABLE roles(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(20) NOT NULL
);


-- сотрудники
CREATE TABLE staff(
    id INT PRIMARY KEY AUTO_INCREMENT,
    surname VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    roleId INT,
    FOREIGN KEY (roleId) REFERENCES roles(id) ON DELETE SET NULL

);

-- категории оборудования
CREATE TABLE equipmentCategory(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL
);

-- статусы оборудования - работает, нуждается в ремонте
CREATE TABLE equipmentStatus(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(10) NOT NULL
);

-- оборудование
CREATE TABLE equipment(
    id INT PRIMARY KEY AUTO_INCREMENT,
    categoryId INT,
    serialNo VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(40) NOT NULL,
    statusId INT,
    FOREIGN KEY (categoryId) REFERENCES equipmentCategory(id),
    FOREIGN KEY (statusId) REFERENCES equipmentStatus(id)
);




-- статусы обслуживания оборудования
CREATE TABLE maintenanceStatus(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(20) NOT NULL
);

-- плановое обслуживание оборудования
CREATE TABLE equipmentMaintenance(
    id INT PRIMARY KEY AUTO_INCREMENT,
    equipmentId INT,
    maintenanceDate DATE NOT NULL,
    statusId INT,
    staffId INT,
    FOREIGN KEY (equipmentId) REFERENCES equipment(id),
    FOREIGN KEY (statusId) REFERENCES maintenanceStatus(id),
    FOREIGN KEY (staffId) REFERENCES staff(id)
);


-- статусы закупки оборудования - заявка создана, закупка завершена, отменена
CREATE TABLE purchaseStatus(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(15) NOT NULL
);

-- закупки оборудования
CREATE TABLE purchase(
    id INT PRIMARY KEY AUTO_INCREMENT,
    purchaseDate DATE NOT NULL,
    statusId INT,
    equipmentId INT,
    quantity INT NOT NULL DEFAULT 1, 
    cost DECIMAL(10,2) NOT NULL,   
    FOREIGN KEY (statusId) REFERENCES purchaseStatus(id),
    FOREIGN KEY (equipmentId) REFERENCES equipment(id)
);