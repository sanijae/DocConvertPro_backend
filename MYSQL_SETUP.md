# MySQL Database Setup Guide

This guide will help you set up MySQL database for the DocConvertPro backend.

## Prerequisites

- MySQL Server 5.7+ or MariaDB 10.3+
- Python 3.9+
- Virtual environment activated

## Installation

### Windows

1. Download MySQL Installer from [MySQL Downloads](https://dev.mysql.com/downloads/mysql/)
2. Run the installer and follow the setup wizard
3. Remember the root password you set during installation
4. MySQL service should start automatically

### macOS

```bash
# Using Homebrew
brew install mysql
brew services start mysql

# Or download from MySQL website
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Linux (CentOS/RHEL)

```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

## Database Setup

### 1. Access MySQL

```bash
# Windows (if MySQL is in PATH)
mysql -u root -p

# macOS/Linux
mysql -u root -p
```

### 2. Create Database and User

```sql
-- Create database with UTF-8 support
CREATE DATABASE doconva_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'doconva_user'@'localhost' IDENTIFIED BY 'your-secure-password';

-- Grant privileges
GRANT ALL PRIVILEGES ON doconva_db.* TO 'doconva_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT user, host FROM mysql.user WHERE user = 'doconva_user';
```

### 3. Test Connection

```bash
mysql -u doconva_user -p doconva_db
```

## Python Dependencies

### Install MySQL Client Library

The project uses PyMySQL which works on all platforms:

```bash
pip install -r requirements.txt
```

This will install:
- `PyMySQL>=1.1.0` - Pure Python MySQL client (works on Windows, macOS, Linux)
- `mysqlclient>=2.2.0` - C-based MySQL client (optional, for better performance on non-Windows)

**Note**: On Windows, PyMySQL is used automatically. On Linux/macOS, mysqlclient is preferred but PyMySQL will work as a fallback.

## Environment Configuration

### 1. Create `.env` File

Create a `.env` file in the project root (`DocConvertPro_backend/.env`):

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DJANGO_ENVIRONMENT=development
DEBUG=True

# MySQL Database Configuration
DB_NAME=doconva_db
DB_USER=doconva_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306

# Other settings...
```

### 2. Load Environment Variables

Make sure your `.env` file is being loaded. If you're using `python-dotenv`, add this to your `manage.py` or settings:

```python
from dotenv import load_dotenv
load_dotenv()
```

Or use environment variables directly in your system.

## Migration from SQLite

If you're migrating from SQLite to MySQL:

### 1. Backup SQLite Data (if needed)

```bash
# Export data to JSON
python manage.py dumpdata > backup.json
```

### 2. Update Settings

The database settings have been updated in `config/settings/base.py` to use MySQL.

### 3. Run Migrations

```bash
# Create fresh migrations (if needed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Load Data (if you exported)

```bash
# Load data from backup
python manage.py loaddata backup.json
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

## Verify Installation

### 1. Test Database Connection

```bash
python manage.py dbshell
```

This should connect to MySQL. Type `exit` to leave.

### 2. Check Tables

```sql
USE doconva_db;
SHOW TABLES;
```

### 3. Run Server

```bash
python manage.py runserver
```

If the server starts without database errors, MySQL is configured correctly!

## Troubleshooting

### Connection Refused

- **Check MySQL is running**:
  ```bash
  # Windows
  net start MySQL80
  
  # macOS
  brew services list
  
  # Linux
  sudo systemctl status mysql
  ```

### Access Denied

- Verify username and password in `.env`
- Check user privileges:
  ```sql
  SHOW GRANTS FOR 'doconva_user'@'localhost';
  ```

### Character Encoding Issues

- Ensure database uses `utf8mb4`:
  ```sql
  ALTER DATABASE doconva_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### PyMySQL Import Error

- Install PyMySQL:
  ```bash
  pip install PyMySQL
  ```

- Verify it's in `requirements.txt` and installed:
  ```bash
  pip list | grep -i pymysql
  ```

### Migration Errors

- If you get "Table already exists" errors:
  ```bash
  python manage.py migrate --fake-initial
  ```

- For fresh start:
  ```bash
  python manage.py migrate --run-syncdb
  ```

## Production Considerations

1. **Use Strong Passwords**: Never use default or weak passwords
2. **Remote Access**: If needed, create user with host '%' but restrict with firewall:
   ```sql
   CREATE USER 'doconva_user'@'%' IDENTIFIED BY 'strong-password';
   GRANT ALL PRIVILEGES ON doconva_db.* TO 'doconva_user'@'%';
   ```
3. **SSL Connections**: Enable SSL for production:
   ```python
   'OPTIONS': {
       'ssl': {
           'ca': '/path/to/ca.pem',
           'cert': '/path/to/client-cert.pem',
           'key': '/path/to/client-key.pem',
       }
   }
   ```
4. **Backup Strategy**: Set up regular database backups
5. **Connection Pooling**: Consider using connection pooling for high traffic

## Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Django MySQL Setup](https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
