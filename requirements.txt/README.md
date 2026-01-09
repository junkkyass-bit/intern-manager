# Gestion des Stagiaires

Desktop application built with Python, CustomTkinter, and MySQL.

## Features
- CRUD stagiaires
- Filter by class
- Change class (bulk)
- Sort by name
- CSV export
- Responsive UI

## Tech Stack
- Python
- CustomTkinter
- MySQL

## Setup

### Prerequisites
- Python 3.x
- MySQL 8.0 or higher

### Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/yourusername/gestion-stagiaires.git
   cd gestion-stagiaires
```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
   cp .env.example .env
```
   
   Edit `.env` with your MySQL credentials:
```
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=gestion_stagiaires
   DB_PORT=3306
```

4. **Create and setup the database:**
```bash
   # Login to MySQL
   mysql -u your_username -p
   
   # Create the database
   CREATE DATABASE gestion_stagiaires;
   exit;
   
   # Import the schema
   mysql -u your_username -p gestion_stagiaires < schema.sql
```

## Run
```bash
python app.py
```

## Database Structure

The application uses three main tables:
- **majors**: Major/specialization information
- **classes**: Class information (linked to majors)
- **stagiaire**: Student/trainee information (linked to classes)