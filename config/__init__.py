"""
Config package.
"""
import pymysql

# PyMySQL compatibility with Django MySQL backend
# This allows PyMySQL to work as mysqlclient replacement
pymysql.install_as_MySQLdb()