# MySQL Connection Troubleshooting Guide

## Error: Access denied for user 'root'@'localhost' (using password: YES)

This error means MySQL is rejecting the password. Here are several solutions:

## Solution 1: Test MySQL Connection Manually

First, verify you can connect to MySQL:

```bash
# Try connecting with the password from .env
mysql -u root -p
# Enter password: sanijae@123
```

If this fails, the password is incorrect.

## Solution 2: Reset MySQL Root Password

### Windows (MySQL 8.0+)

1. **Stop MySQL Service**:
   ```powershell
   net stop MySQL80
   # or
   net stop MySQL
   ```

2. **Start MySQL in Safe Mode** (skip grant tables):
   ```powershell
   mysqld --skip-grant-tables --console
   ```
   Keep this window open.

3. **Open a new terminal** and connect without password:
   ```powershell
   mysql -u root
   ```

4. **Reset the password**:
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'sanijae@123';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. **Stop the safe mode MySQL** (Ctrl+C in the first terminal)

6. **Start MySQL normally**:
   ```powershell
   net start MySQL80
   ```

7. **Test connection**:
   ```powershell
   mysql -u root -p
   # Enter: sanijae@123
   ```

## Solution 3: Create a New MySQL User (Recommended)

Instead of using root, create a dedicated user for the application:

1. **Connect to MySQL** (you may need to use root without password or with correct password):
   ```bash
   mysql -u root -p
   ```

2. **Create database and user**:
   ```sql
   -- Create database
   CREATE DATABASE IF NOT EXISTS doconva_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- Create user
   CREATE USER 'doconva_user'@'localhost' IDENTIFIED BY 'sanijae@123';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON doconva_db.* TO 'doconva_user'@'localhost';
   
   -- Apply changes
   FLUSH PRIVILEGES;
   
   -- Verify
   SHOW DATABASES;
   SELECT user, host FROM mysql.user WHERE user = 'doconva_user';
   EXIT;
   ```

3. **Update .env file**:
   ```env
   DB_NAME=doconva_db
   DB_USER=doconva_user
   DB_PASSWORD=sanijae@123
   DB_HOST=localhost
   DB_PORT=3306
   ```

## Solution 4: Check MySQL Authentication Plugin

MySQL 8.0+ uses `caching_sha2_password` by default, which PyMySQL supports. However, if you're having issues:

1. **Check current authentication method**:
   ```sql
   SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
   ```

2. **If needed, change to mysql_native_password** (older but more compatible):
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'sanijae@123';
   FLUSH PRIVILEGES;
   ```

## Solution 5: Use MySQL Workbench or phpMyAdmin

If command line is difficult, use a GUI tool:
- **MySQL Workbench**: Download from MySQL website
- **phpMyAdmin**: If you have XAMPP/WAMP installed
- **HeidiSQL**: Free Windows MySQL client

## Solution 6: Check if MySQL is Running

```powershell
# Check MySQL service status
Get-Service | Where-Object {$_.Name -like "*mysql*"}

# Start MySQL if stopped
net start MySQL80
# or
net start MySQL
```

## Solution 7: Verify .env File is Being Loaded

Test if environment variables are loaded:

```python
# Create test script: test_env.py
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
```

Run: `python test_env.py`

## Quick Fix Script

Create a file `fix_mysql.py`:

```python
import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'doconva_db'),
        port=int(os.getenv('DB_PORT', 3306)),
        charset='utf8mb4'
    )
    print("✅ Connection successful!")
    connection.close()
except pymysql.Error as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting steps:")
    print("1. Verify MySQL is running")
    print("2. Check username and password")
    print("3. Ensure database exists")
    print("4. Check user privileges")
```

## Common Issues

### Issue: Password contains special characters
If your password has `@`, `#`, `$`, etc., make sure it's properly quoted in .env:
```env
DB_PASSWORD="sanijae@123"
```

### Issue: MySQL not installed
Download and install MySQL from: https://dev.mysql.com/downloads/mysql/

### Issue: Port 3306 is blocked
Check if another service is using port 3306:
```powershell
netstat -ano | findstr :3306
```

## Next Steps After Fixing

Once connection works:

1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Test server**:
   ```bash
   python manage.py runserver
   ```
