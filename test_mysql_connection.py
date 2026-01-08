"""
Test MySQL connection script.
Run this to diagnose MySQL connection issues.
"""
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

print("=" * 60)
print("MySQL Connection Test")
print("=" * 60)
print()

# Display configuration
print("Configuration from .env:")
print(f"  DB_NAME: {os.getenv('DB_NAME', 'NOT SET')}")
print(f"  DB_USER: {os.getenv('DB_USER', 'NOT SET')}")
print(f"  DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', '')) if os.getenv('DB_PASSWORD') else 'NOT SET'}")
print(f"  DB_HOST: {os.getenv('DB_HOST', 'NOT SET')}")
print(f"  DB_PORT: {os.getenv('DB_PORT', 'NOT SET')}")
print()

# Test PyMySQL import
try:
    import pymysql
    print("✅ PyMySQL is installed")
    print(f"   Version: {pymysql.__version__}")
except ImportError:
    print("❌ PyMySQL is NOT installed")
    print("   Run: pip install PyMySQL")
    sys.exit(1)

print()

# Test connection
print("Attempting to connect to MySQL...")
try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'doconva_db'),
        port=int(os.getenv('DB_PORT', 3306)),
        charset='utf8mb4',
        connect_timeout=10
    )
    
    print("✅ Connection successful!")
    print()
    
    # Test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"   MySQL Version: {version[0]}")
        
        cursor.execute("SELECT DATABASE()")
        db = cursor.fetchone()
        print(f"   Current Database: {db[0] if db[0] else 'None'}")
        
        cursor.execute("SELECT USER()")
        user = cursor.fetchone()
        print(f"   Connected as: {user[0]}")
    
    connection.close()
    print()
    print("=" * 60)
    print("✅ All tests passed! Your MySQL connection is working.")
    print("=" * 60)
    
except pymysql.Error as e:
    print(f"❌ Connection failed!")
    print()
    print(f"Error: {e}")
    print()
    print("=" * 60)
    print("Troubleshooting Steps:")
    print("=" * 60)
    print()
    
    error_code = e.args[0] if e.args else None
    
    if error_code == 1045:
        print("❌ Error 1045: Access denied (wrong username/password)")
        print()
        print("Solutions:")
        print("1. Verify MySQL root password:")
        print("   - Open MySQL Workbench or phpMyAdmin")
        print("   - Try logging in with root and your password")
        print("   - If login fails, password is incorrect")
        print()
        print("2. Reset MySQL root password:")
        print("   - Stop MySQL service: net stop MySQL80")
        print("   - Start in safe mode: mysqld --skip-grant-tables")
        print("   - Connect: mysql -u root")
        print("   - Run: ALTER USER 'root'@'localhost' IDENTIFIED BY 'your-password';")
        print()
        print("3. Create a new MySQL user (recommended):")
        print("   - Connect to MySQL as root")
        print("   - Run:")
        print("     CREATE DATABASE doconva_db;")
        print("     CREATE USER 'doconva_user'@'localhost' IDENTIFIED BY 'sanijae@123';")
        print("     GRANT ALL PRIVILEGES ON doconva_db.* TO 'doconva_user'@'localhost';")
        print("     FLUSH PRIVILEGES;")
        print("   - Update .env: DB_USER=doconva_user")
        
    elif error_code == 2003:
        print("❌ Error 2003: Can't connect to MySQL server")
        print()
        print("Solutions:")
        print("1. Check if MySQL service is running:")
        print("   Get-Service | Where-Object {$_.Name -like '*mysql*'}")
        print("   net start MySQL80")
        print()
        print("2. Verify MySQL is installed:")
        print("   - Check if MySQL is in Program Files")
        print("   - Or install MySQL from: https://dev.mysql.com/downloads/mysql/")
        
    elif error_code == 1049:
        print("❌ Error 1049: Unknown database")
        print()
        print("Solution: Create the database:")
        print("  CREATE DATABASE doconva_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
    else:
        print(f"❌ Error {error_code}: {e}")
        print()
        print("General solutions:")
        print("1. Verify MySQL is installed and running")
        print("2. Check .env file has correct credentials")
        print("3. Ensure database exists")
        print("4. Check user has proper permissions")
    
    print()
    print("For detailed help, see: MYSQL_TROUBLESHOOTING.md")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"   Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
