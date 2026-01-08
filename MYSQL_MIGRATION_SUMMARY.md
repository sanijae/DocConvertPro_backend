# MySQL Migration Summary

This document summarizes the changes made to migrate the backend from SQLite to MySQL.

## Changes Made

### 1. Database Configuration (`config/settings/base.py`)

**Before:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**After:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'doconva_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 2. PyMySQL Initialization (`config/__init__.py`)

Added PyMySQL compatibility layer:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

This allows PyMySQL to work as a drop-in replacement for mysqlclient, especially useful on Windows.

### 3. Dependencies (`requirements.txt`)

Added MySQL client libraries:
```
# MySQL Database
PyMySQL>=1.1.0
mysqlclient>=2.2.0; platform_system != "Windows"
```

- **PyMySQL**: Pure Python MySQL client (works on all platforms)
- **mysqlclient**: C-based MySQL client (better performance, but not available on Windows)

### 4. Documentation Updates

- **README.md**: Updated database sections to reflect MySQL usage
- **MYSQL_SETUP.md**: Created comprehensive MySQL setup guide

## Required Environment Variables

Add these to your `.env` file:

```env
DB_NAME=doconva_db
DB_USER=doconva_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

## Next Steps

1. **Install MySQL Server** (if not already installed)
   - See `MYSQL_SETUP.md` for platform-specific instructions

2. **Create Database and User**:
   ```sql
   CREATE DATABASE doconva_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'doconva_user'@'localhost' IDENTIFIED BY 'your-password';
   GRANT ALL PRIVILEGES ON doconva_db.* TO 'doconva_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create `.env` file with database credentials
   - Or set environment variables directly

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser** (if needed):
   ```bash
   python manage.py createsuperuser
   ```

## Migration from SQLite (if applicable)

If you have existing SQLite data:

1. **Export Data**:
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Update Settings** (already done)

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Load Data**:
   ```bash
   python manage.py loaddata backup.json
   ```

## Testing

Verify the setup:

```bash
# Test database connection
python manage.py dbshell

# Run server
python manage.py runserver
```

## Notes

- The database uses `utf8mb4` character set for full Unicode support
- PyMySQL is automatically initialized when Django starts
- All database settings are configurable via environment variables
- The old `db.sqlite3` file can be removed after successful migration

## Troubleshooting

See `MYSQL_SETUP.md` for detailed troubleshooting guide.

Common issues:
- **Connection refused**: MySQL service not running
- **Access denied**: Check username/password in `.env`
- **Import error**: Run `pip install -r requirements.txt`
