# Lab Equipment Management System

A lightweight web application for managing laboratory equipment, staff, maintenance schedules, and purchases. Designed for small scientific laboratories where the head of the lab handles all administrative tasks.

## Overview

This application replaces scattered Excel spreadsheets with a structured database and intuitive web interface. It allows centralized storage and management of:

- Laboratory staff and their roles
- Equipment inventory with categories and statuses
- Maintenance scheduling and tracking
- Purchase orders and history

## Technology Stack

- **Backend**: Python 3, Flask
- **Database**: MySQL with phpMyAdmin
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Environment**: Conda, Git
- **OS**: Linux Ubuntu (compatible with Windows)

## Project Structure
```text
lab_equipment_management/
│
├── app.py                 # Main application file with routes
├── config.py              # Database connection settings
├── database.py            # Database operations module
├── create_database.sql    # SQL script for database creation
├── environment.yaml       # Conda environment configuration
│
├── static/
│   └── css/
│       └── style.css      # Application stylesheet
│
└── templates/             # HTML templates
    ├── base.html          # Base template with navigation
    ├── index.html         # Main page with statistics
    ├── staff.html         # Staff management page
    ├── equipment.html     # Equipment management page
    ├── maintenance.html   # Maintenance schedule page
    └── purchases.html     # Purchases management page
```


## Database Schema

The database consists of 8 interconnected tables:

- **staff** & **roles** — laboratory personnel
- **equipment**, **equipmentCategory**, **equipmentStatus** — equipment inventory with catalogs
- **equipmentMaintenance** & **maintenanceStatus** — maintenance scheduling
- **purchase** & **purchaseStatus** — equipment purchasing

Referential integrity is enforced through primary and foreign keys.

## Key Features

- **Staff management** — add, edit, delete staff members and assign roles
- **Equipment tracking** — maintain equipment list with unique serial numbers, categories, and statuses
- **Maintenance scheduling** — plan and track maintenance tasks with assigned personnel
- **Purchase management** — record purchase orders with quantities and costs
- **Dashboard** — view summary statistics (equipment by category, staff by role, upcoming maintenance)
- **CRUD operations** — all operations available directly from table views
- **Flash messages** — user feedback for all actions

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yakushov1/laboratory_equipment
   cd lab_equipment_management

2. **Set up Conda environment**
   ```bash
   conda env create -f environment.yaml
   conda activate kait_lab_equipment
3. **Configure database**
   Create a MySQL database named lab_equipment
   Update config.py with your database credentials
   Run the SQL script:create_database.sql
4. **Run the application**
    ```bash
    python app.py
5. **Access the application**
   Open browser and navigate to http://127.0.0.1:5000
## Usage

The interface is designed for single-user operation (lab head). Each management page follows the same pattern:

- Table view showing all records
- Top row for adding new entries
- Inline editing with "Save" buttons
- "Delete" buttons with confirmation prompts

Navigation menu provides access to all sections:

- **Home** — dashboard with statistics
- **Staff** — manage laboratory personnel
- **Equipment** — manage equipment inventory
- **Maintenance** — schedule and track maintenance
- **Purchases** — manage purchase orders

## Customization

The application uses reference tables for categories and statuses:

- Equipment categories
- Equipment statuses
- Maintenance statuses
- Purchase statuses
- Staff roles

These can be populated according to your laboratory's specific needs.

## Limitations

- Single-user system (no authentication/authorization)
- Designed for local network use
- No integration with external systems (accounting, ERP)
- Basic analytics only

## Future Enhancements

- Export reports to PDF/Excel
- Email/Telegram notifications for upcoming maintenance
- Multi-user support with access levels
- Advanced analytics and charts
- Equipment usage history tracking

## License

This project is developed for educational purposes as part of a course work.
